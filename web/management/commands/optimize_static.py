"""
Django management command to optimize static files for production
Usage: python manage.py optimize_static
"""

import os
import gzip
import shutil
import hashlib
import json
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage


class Command(BaseCommand):
    help = 'Optimize static files for production deployment'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            default='static_optimized',
            help='Output directory for optimized files'
        )
        parser.add_argument(
            '--compress',
            action='store_true',
            help='Create gzip compressed versions of files'
        )
        parser.add_argument(
            '--manifest',
            action='store_true',
            help='Generate cache-busting manifest file'
        )
        parser.add_argument(
            '--bundle',
            action='store_true',
            help='Bundle JavaScript and CSS files'
        )
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Clean output directory before optimization'
        )

    def handle(self, *args, **options):
        self.output_dir = Path(options['output'])
        self.compress = options['compress']
        self.manifest = options['manifest']
        self.bundle = options['bundle']
        
        self.stdout.write(
            self.style.SUCCESS('🏗️  Starting static files optimization...')
        )
        
        try:
            # Clean output directory if requested
            if options['clean'] and self.output_dir.exists():
                shutil.rmtree(self.output_dir)
                self.stdout.write(f"Cleaned output directory: {self.output_dir}")
            
            # Create output directory
            self.output_dir.mkdir(exist_ok=True)
            
            # Find all static files
            static_files = self.find_static_files()
            
            # Process files
            if self.bundle:
                self.bundle_files(static_files)
            else:
                self.copy_files(static_files)
            
            # Compress files if requested
            if self.compress:
                self.compress_files()
            
            # Generate manifest if requested
            if self.manifest:
                self.generate_manifest()
            
            # Generate optimization report
            self.generate_report()
            
            self.stdout.write(
                self.style.SUCCESS('✅ Static files optimization completed!')
            )
            
        except Exception as e:
            raise CommandError(f'Optimization failed: {str(e)}')

    def find_static_files(self):
        """Find all static files in the project"""
        self.stdout.write("📁 Finding static files...")
        
        static_files = {}
        
        # Use Django's static files finder
        for finder in finders.get_finders():
            for path, storage in finder.list([]):
                if path.endswith(('.js', '.css', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico')):
                    full_path = finder.find(path)
                    if full_path:
                        static_files[path] = full_path
        
        self.stdout.write(f"Found {len(static_files)} static files")
        return static_files

    def copy_files(self, static_files):
        """Copy static files to output directory"""
        self.stdout.write("📋 Copying static files...")
        
        for relative_path, full_path in static_files.items():
            output_path = self.output_dir / relative_path
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.copy2(full_path, output_path)
        
        self.stdout.write(f"Copied {len(static_files)} files")

    def bundle_files(self, static_files):
        """Bundle JavaScript and CSS files"""
        self.stdout.write("📦 Bundling files...")
        
        # Separate files by type
        js_files = {k: v for k, v in static_files.items() if k.endswith('.js')}
        css_files = {k: v for k, v in static_files.items() if k.endswith('.css')}
        other_files = {k: v for k, v in static_files.items() 
                      if not k.endswith(('.js', '.css'))}
        
        # Bundle JavaScript files
        if js_files:
            self.bundle_js_files(js_files)
        
        # Bundle CSS files
        if css_files:
            self.bundle_css_files(css_files)
        
        # Copy other files
        self.copy_files(other_files)

    def bundle_js_files(self, js_files):
        """Bundle JavaScript files"""
        self.stdout.write("🔧 Bundling JavaScript files...")
        
        # Group by app/directory
        js_groups = {}
        for path, full_path in js_files.items():
            # Extract app name from path
            parts = Path(path).parts
            if len(parts) > 1:
                app_name = parts[0]
            else:
                app_name = 'global'
            
            if app_name not in js_groups:
                js_groups[app_name] = []
            js_groups[app_name].append((path, full_path))
        
        # Create bundles for each group
        for app_name, files in js_groups.items():
            bundle_content = []
            
            for path, full_path in files:
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        bundle_content.append(f"/* {path} */\n{content}\n")
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f"Warning: Could not read {path}: {e}")
                    )
            
            if bundle_content:
                bundle_path = self.output_dir / f"{app_name}-bundle.js"
                bundle_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(bundle_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(bundle_content))
                
                self.stdout.write(f"Created JS bundle: {bundle_path}")

    def bundle_css_files(self, css_files):
        """Bundle CSS files"""
        self.stdout.write("🎨 Bundling CSS files...")
        
        # Group by app/directory
        css_groups = {}
        for path, full_path in css_files.items():
            # Extract app name from path
            parts = Path(path).parts
            if len(parts) > 1:
                app_name = parts[0]
            else:
                app_name = 'global'
            
            if app_name not in css_groups:
                css_groups[app_name] = []
            css_groups[app_name].append((path, full_path))
        
        # Create bundles for each group
        for app_name, files in css_groups.items():
            bundle_content = []
            
            for path, full_path in files:
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        bundle_content.append(f"/* {path} */\n{content}\n")
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f"Warning: Could not read {path}: {e}")
                    )
            
            if bundle_content:
                bundle_path = self.output_dir / f"{app_name}-bundle.css"
                bundle_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(bundle_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(bundle_content))
                
                self.stdout.write(f"Created CSS bundle: {bundle_path}")

    def compress_files(self):
        """Create gzip compressed versions of text files"""
        self.stdout.write("🗜️  Compressing files...")
        
        compressed_count = 0
        total_savings = 0
        
        for file_path in self.output_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix in ['.js', '.css', '.html', '.txt', '.json']:
                gz_path = file_path.with_suffix(file_path.suffix + '.gz')
                
                try:
                    with open(file_path, 'rb') as f_in:
                        with gzip.open(gz_path, 'wb', compresslevel=9) as f_out:
                            data = f_in.read()
                            f_out.write(data)
                    
                    # Calculate compression ratio
                    original_size = len(data)
                    compressed_size = gz_path.stat().st_size
                    savings = original_size - compressed_size
                    total_savings += savings
                    
                    ratio = (savings / original_size) * 100 if original_size > 0 else 0
                    
                    if ratio > 10:  # Only log significant compression
                        self.stdout.write(
                            f"Compressed {file_path.name}: {ratio:.1f}% reduction"
                        )
                    
                    compressed_count += 1
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f"Could not compress {file_path}: {e}")
                    )
        
        self.stdout.write(
            f"Compressed {compressed_count} files, saved {total_savings / 1024:.1f} KB"
        )

    def generate_manifest(self):
        """Generate asset manifest for cache busting"""
        self.stdout.write("📋 Generating asset manifest...")
        
        manifest = {}
        
        for file_path in self.output_dir.rglob("*"):
            if file_path.is_file() and not file_path.name.endswith('.gz'):
                # Calculate file hash
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()[:8]
                
                # Create relative path
                rel_path = file_path.relative_to(self.output_dir)
                
                # Create versioned filename
                name = file_path.stem
                ext = file_path.suffix
                versioned_name = f"{name}.{file_hash}{ext}"
                
                manifest[str(rel_path)] = str(rel_path.parent / versioned_name)
        
        # Write manifest
        manifest_path = self.output_dir / "manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)
        
        self.stdout.write(f"Generated manifest with {len(manifest)} entries")

    def generate_report(self):
        """Generate optimization report"""
        self.stdout.write("📊 Generating optimization report...")
        
        report = {
            'timestamp': str(Path().cwd()),
            'output_directory': str(self.output_dir),
            'files': {},
            'summary': {}
        }
        
        total_files = 0
        total_size = 0
        file_types = {}
        
        for file_path in self.output_dir.rglob("*"):
            if file_path.is_file() and not file_path.name.endswith('.gz'):
                size = file_path.stat().st_size
                ext = file_path.suffix.lower()
                
                total_files += 1
                total_size += size
                
                if ext not in file_types:
                    file_types[ext] = {'count': 0, 'size': 0}
                file_types[ext]['count'] += 1
                file_types[ext]['size'] += size
                
                rel_path = file_path.relative_to(self.output_dir)
                report['files'][str(rel_path)] = {
                    'size': size,
                    'type': ext
                }
        
        report['summary'] = {
            'total_files': total_files,
            'total_size': total_size,
            'file_types': file_types
        }
        
        # Write report
        report_path = self.output_dir / "optimization_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        self.stdout.write("\n📊 Optimization Summary:")
        self.stdout.write(f"Total files: {total_files}")
        self.stdout.write(f"Total size: {total_size / 1024:.1f} KB")
        
        for ext, info in sorted(file_types.items()):
            self.stdout.write(
                f"{ext or 'no extension'}: {info['count']} files, "
                f"{info['size'] / 1024:.1f} KB"
            )
        
        self.stdout.write(f"Report saved to: {report_path}")
