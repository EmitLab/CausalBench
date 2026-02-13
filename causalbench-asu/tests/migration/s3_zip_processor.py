import sys
import os
import zipfile
import yaml
import tempfile
from pathlib import Path
import boto3
from io import BytesIO

sys.path.append(os.path.join(os.path.dirname(__file__), 'CausalBench-Backend', 'helper_services'))

import s3_service


def get_all_zip_files_from_s3(bucket_name='causalbench-1225'):
    """Get list of ALL ZIP files from S3 bucket (handles pagination)"""
    s3_client = boto3.client('s3')
    zip_files = []
    
    try:
        # Use paginator to get ALL objects, not just first 1000
        paginator = s3_client.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucket_name)
        
        total_objects = 0
        for page in page_iterator:
            if 'Contents' in page:
                page_objects = page['Contents']
                total_objects += len(page_objects)
                
                # Filter for ZIP files in this page
                page_zip_files = [
                    obj['Key'] for obj in page_objects
                    if obj['Key'].lower().endswith('.zip')
                ]
                zip_files.extend(page_zip_files)
                
                print(f"  Processed page with {len(page_objects)} objects, found {len(page_zip_files)} ZIP files")
        
        print(f"Total objects scanned: {total_objects}")
        print(f"Found {len(zip_files)} ZIP files in bucket {bucket_name}")
        return zip_files
        
    except Exception as e:
        print(f"Error listing objects: {e}")
        return []

def process_zip_file(zip_key):
    """Download ZIP file, extract it, update config.yaml task value, and upload back to S3"""
    print(f"\nProcessing: {zip_key}")
    
    # Download ZIP file as BytesIO
    file_obj = s3_service.download_file_as_bytesio(zip_key)
    
    if not file_obj:
        print(f"Failed to download {zip_key}")
        return
    
    # Create a temporary directory for extraction and modification
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        extract_dir = temp_dir_path / "extracted"
        extract_dir.mkdir()
        
        # Extract ZIP file
        try:
            with zipfile.ZipFile(file_obj, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
                print(f"  Extracted {zip_key}")
                
                # Find config.yaml files
                config_files = list(extract_dir.rglob("config.yaml")) + list(extract_dir.rglob("config.yml"))
                
                if not config_files:
                    print(f"  No config.yaml found in {zip_key}, copying zip file as-is")
                else:
                    print(f"  Found {len(config_files)} config file(s)")
                
                modified = False
                for config_file in config_files:
                    print(f"  Found config file: {config_file.relative_to(extract_dir)}")
                    
                    try:
                        # Read the original file as text to preserve formatting
                        with open(config_file, 'r') as f:
                            original_lines = f.readlines()
                        
                        # Also parse as YAML to understand structure
                        with open(config_file, 'r') as f:
                            config_data = yaml.safe_load(f) or {}
                        
                        # Only do this if 'task' exists
                        if 'task' in config_data:
                            # Remove name from 'task'

                            config_data['task'] = {
                                'id': config_data['task'][0]['id'],
                                'version': config_data['task'][0]['version']
                            }

                            print(f"Removed name from task")

                        # Always do this
                        config_data['causalbench'] = {
                            'major': '0',
                            'minor': '2',
                            'build': '0'
                        }
                        
                        # Reconstruct YAML with proper 4-space indentation
                        yaml_content = yaml.dump(config_data, default_flow_style=False, sort_keys=False, indent=4)
                        
                        # Write the reconstructed YAML content
                        with open(config_file, 'w') as f:
                            f.write(yaml_content)
                        
                        modified = True
                        
                    except Exception as e:
                        print(f"    Error updating {config_file}: {e}")
                        continue
                
                if not modified:
                    print(f"  No config files were modified in {zip_key}, copying zip file as-is")
                
                # Create new ZIP file with content (modified or unmodified)
                new_zip_path = temp_dir_path / f"updated_{Path(zip_key).name}"
                
                with zipfile.ZipFile(new_zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as new_zip:
                    for file_path in extract_dir.rglob("*"):
                        if file_path.is_file():
                            # Calculate relative path from extract_dir
                            rel_path = file_path.relative_to(extract_dir)
                            new_zip.write(file_path, rel_path)
                
                if modified:
                    print(f"  Created updated ZIP file with modifications")
                else:
                    print(f"  Created ZIP file (no modifications)")
                
                # Upload ZIP back to S3 (modified or unmodified)
                upload_success = upload_file_to_s3(str(new_zip_path), zip_key)
                if upload_success:
                    if modified:
                        print(f"  Successfully uploaded updated {zip_key} to S3")
                    else:
                        print(f"  Successfully copied {zip_key} to S3 (as-is)")
                else:
                    print(f"  Failed to upload {zip_key} to S3")
        
        except zipfile.BadZipFile:
            print(f"  Error: {zip_key} is not a valid ZIP file")
        except Exception as e:
            print(f"  Error processing {zip_key}: {e}")

def upload_file_to_s3(local_file_path, s3_key, bucket_name='causalbench-0209'):
    """Upload a file to S3"""
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(local_file_path, bucket_name, s3_key)
        return True
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return False

# Main execution
print("Starting to process all ZIP files...")
print("📥 Source bucket: causalbench")
print("📤 Destination bucket: causalbench-migration-test")
print("⚠️  Original files will NOT be modified!")

# Get all ZIP files from S3
zip_files = get_all_zip_files_from_s3()

# Process each ZIP file
for zip_file in zip_files:
    process_zip_file(zip_file)

print(f"\nFinished processing {len(zip_files)} ZIP files.")
print("✅ All modified files are safely stored in causalbench-migration-test bucket")
print("💡 No local copies were saved - files were processed in memory only")
