#!/usr/bin/env python3
"""
OpenAPI Specification Splitter for watsonx Orchestrate

This script splits the monolithic openapi.json into individual files per endpoint.
This allows you to upload/update individual API endpoints in watsonx Orchestrate
without having to re-upload the entire specification.

Usage:
    python3 split_openapi.py
    
Output:
    Creates openapi_endpoints/ directory with individual JSON files:
    - openapi_analyze_energy.json
    - openapi_anomaly_detection.json
    - openapi_energy_forecast.json
    - openapi_simulation_run.json
    - openapi_what_if.json
    - openapi_maintenance_schedule.json
    - openapi_chatops.json
    - etc.

Each file contains:
    - Full OpenAPI 3.1.0 structure
    - Single path/endpoint
    - All required schemas/components for that endpoint
    - Server information
    - Authentication details

Benefits:
    ✅ Update single API without re-uploading entire spec
    ✅ Faster iterations during development
    ✅ Easier to manage in watsonx Orchestrate Skills Catalog
    ✅ Reduces risk of breaking other APIs during updates
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Set


def load_openapi_spec(filepath: str = "openapi.json") -> dict:
    """Load the OpenAPI specification from file"""
    with open(filepath, 'r') as f:
        return json.load(f)


def extract_referenced_schemas(operation: dict, spec: dict) -> Dict[str, dict]:
    """
    Extract all schemas referenced by an operation (request body, responses, parameters)
    Recursively follows $ref to include nested schemas
    """
    schemas = {}
    refs_to_process = set()
    
    def add_ref(ref: str):
        """Add a $ref to the processing queue"""
        if ref.startswith("#/components/schemas/"):
            schema_name = ref.split("/")[-1]
            refs_to_process.add(schema_name)
    
    def scan_for_refs(obj):
        """Recursively scan object for $ref"""
        if isinstance(obj, dict):
            if "$ref" in obj:
                add_ref(obj["$ref"])
            for value in obj.values():
                scan_for_refs(value)
        elif isinstance(obj, list):
            for item in obj:
                scan_for_refs(item)
    
    # Scan operation for refs
    scan_for_refs(operation)
    
    # Process all refs recursively
    processed = set()
    while refs_to_process:
        schema_name = refs_to_process.pop()
        if schema_name in processed:
            continue
        
        processed.add(schema_name)
        
        # Get schema from spec
        if schema_name in spec.get("components", {}).get("schemas", {}):
            schema_def = spec["components"]["schemas"][schema_name]
            schemas[schema_name] = schema_def
            
            # Scan this schema for more refs
            scan_for_refs(schema_def)
    
    return schemas


def create_endpoint_spec(path: str, method: str, operation: dict, base_spec: dict) -> dict:
    """
    Create a standalone OpenAPI spec for a single endpoint
    """
    # Extract referenced schemas
    schemas = extract_referenced_schemas(operation, base_spec)
    
    # Build minimal OpenAPI spec
    endpoint_spec = {
        "openapi": base_spec.get("openapi", "3.1.0"),
        "info": {
            "title": f"{base_spec['info']['title']} - {operation.get('summary', path)}",
            "description": operation.get("description", f"API endpoint: {method.upper()} {path}"),
            "version": base_spec["info"]["version"]
        },
        "servers": base_spec.get("servers", []),
        "paths": {
            path: {
                method: operation
            }
        }
    }
    
    # Add components if schemas exist
    if schemas:
        endpoint_spec["components"] = {
            "schemas": schemas
        }
    
    # Add security schemes if present
    if "components" in base_spec and "securitySchemes" in base_spec["components"]:
        if "components" not in endpoint_spec:
            endpoint_spec["components"] = {}
        endpoint_spec["components"]["securitySchemes"] = base_spec["components"]["securitySchemes"]
    
    # Add security if present in operation or globally
    if "security" in operation:
        endpoint_spec["security"] = operation["security"]
    elif "security" in base_spec:
        endpoint_spec["security"] = base_spec["security"]
    
    return endpoint_spec


def sanitize_filename(path: str, method: str) -> str:
    """
    Convert API path to safe filename
    Example: /api/analyze-energy -> openapi_analyze_energy.json
    """
    # Remove leading/trailing slashes and /api prefix
    clean_path = path.strip("/").replace("/api/", "")
    
    # Replace remaining slashes and special chars with underscores
    clean_path = clean_path.replace("/", "_").replace("-", "_").replace("{", "").replace("}", "")
    
    # Add method if not GET (for clarity on POST/PUT/DELETE)
    if method.lower() != "get":
        filename = f"openapi_{clean_path}_{method.lower()}.json"
    else:
        filename = f"openapi_{clean_path}.json"
    
    return filename


def split_openapi(input_file: str = "openapi.json", output_dir: str = "openapi_endpoints") -> List[str]:
    """
    Split OpenAPI spec into individual endpoint files
    Returns list of created files
    """
    # Load spec
    print(f"📖 Loading OpenAPI spec from {input_file}...")
    spec = load_openapi_spec(input_file)
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    print(f"📁 Output directory: {output_path.absolute()}")
    
    created_files = []
    
    # Process each path and method
    paths = spec.get("paths", {})
    total_endpoints = sum(len(methods) for methods in paths.values())
    
    print(f"\n🔍 Found {len(paths)} paths with {total_endpoints} total endpoints")
    print("─" * 60)
    
    for path, methods in paths.items():
        for method, operation in methods.items():
            if method.lower() in ['get', 'post', 'put', 'delete', 'patch']:
                # Generate filename
                filename = sanitize_filename(path, method)
                output_file = output_path / filename
                
                # Create endpoint spec
                endpoint_spec = create_endpoint_spec(path, method, operation, spec)
                
                # Write to file
                with open(output_file, 'w') as f:
                    json.dump(endpoint_spec, f, indent=2)
                
                created_files.append(str(output_file))
                
                # Print info
                summary = operation.get("summary", path)
                print(f"✅ {method.upper():6} {path:40} → {filename}")
    
    print("─" * 60)
    print(f"\n✨ Successfully created {len(created_files)} endpoint files!")
    print(f"📂 Location: {output_path.absolute()}")
    
    # Create index file
    create_index_file(output_path, created_files, spec)
    
    return created_files


def create_index_file(output_path: Path, created_files: List[str], spec: dict):
    """
    Create an index.json file listing all endpoints
    Useful for documentation and bulk operations
    """
    index = {
        "project": spec["info"]["title"],
        "version": spec["info"]["version"],
        "total_endpoints": len(created_files),
        "endpoints": []
    }
    
    for filepath in sorted(created_files):
        with open(filepath, 'r') as f:
            endpoint_spec = json.load(f)
        
        # Extract info
        path = list(endpoint_spec["paths"].keys())[0]
        method = list(endpoint_spec["paths"][path].keys())[0]
        operation = endpoint_spec["paths"][path][method]
        
        index["endpoints"].append({
            "file": Path(filepath).name,
            "method": method.upper(),
            "path": path,
            "summary": operation.get("summary", ""),
            "tags": operation.get("tags", [])
        })
    
    index_file = output_path / "index.json"
    with open(index_file, 'w') as f:
        json.dump(index, f, indent=2)
    
    print(f"\n📋 Created index file: {index_file.name}")


def create_readme(output_path: Path):
    """Create README explaining how to use split files"""
    readme_content = """# OpenAPI Endpoint Files

This directory contains individual OpenAPI specification files for each API endpoint.

## Purpose

Instead of uploading the entire monolithic `openapi.json` file to watsonx Orchestrate, you can upload individual endpoint files. This allows you to:

✅ Update a single API without affecting others
✅ Faster iteration during development  
✅ Easier management in watsonx Skills Catalog
✅ Reduced risk of breaking working APIs

## How to Use

### Upload to watsonx Orchestrate

1. Go to watsonx Orchestrate Skills Catalog
2. Click "Add Skill" → "OpenAPI"
3. Upload the individual endpoint file (e.g., `openapi_analyze_energy_post.json`)
4. Configure the skill name and authentication
5. Test the skill

### Update an Existing Skill

1. Regenerate the split files: `python3 split_openapi.py`
2. In watsonx Orchestrate, go to Skills Catalog
3. Find the skill you want to update
4. Click "Edit" → "Update OpenAPI Spec"
5. Upload the new endpoint file
6. Test to verify changes

## File Naming Convention

Files are named based on the API path and HTTP method:

- `openapi_analyze_energy_post.json` → `POST /api/analyze-energy`
- `openapi_anomaly_detection_post.json` → `POST /api/ml/anomaly-detection`
- `openapi_zones_status_get.json` → `GET /api/zones/status`

## Priority Endpoints for watsonx

These are the most important endpoints to upload first:

1. **openapi_analyze_energy_post.json** - Energy analysis workflow
2. **openapi_anomaly_detection_post.json** - Anomaly detection
3. **openapi_energy_forecast_post.json** - Energy forecasting
4. **openapi_simulation_run_post.json** - Digital twin simulation
5. **openapi_what_if_post.json** - What-if scenario analysis
6. **openapi_maintenance_schedule_post.json** - Maintenance scheduling
7. **openapi_chatops_post.json** - Natural language queries

## Index File

`index.json` contains a catalog of all endpoints with metadata. Use this to:

- See all available endpoints at a glance
- Script bulk operations
- Generate documentation

## Regenerating Files

When you make changes to your API:

```bash
# Update the main OpenAPI spec
python3 -c "from backend.app import app; import json; spec = app.openapi(); print(json.dumps(spec, indent=2))" > openapi.json

# Split into individual files
python3 split_openapi.py
```

## Troubleshooting

**Issue**: Endpoint file missing schemas

→ Make sure your API uses Pydantic models with proper type hints

**Issue**: watsonx can't parse the file

→ Verify JSON is valid: `jq . openapi_endpoint_name.json`

**Issue**: Authentication not working

→ Check that securitySchemes are included in the endpoint file

## Support

For issues or questions, see:
- Main README.md
- WATSONX_AGENT_TRAINING_GUIDE.md
- WATSONX_EMBEDDING_GUIDE.md
"""
    
    readme_file = output_path / "README.md"
    with open(readme_file, 'w') as f:
        f.write(readme_content)
    
    print(f"📚 Created README: {readme_file.name}")


def main():
    """Main entry point"""
    print("🚀 OpenAPI Specification Splitter")
    print("=" * 60)
    
    # Check if openapi.json exists
    if not os.path.exists("openapi.json"):
        print("\n❌ Error: openapi.json not found!")
        print("\nGenerate it first with:")
        print('python3 -c "from backend.app import app; import json; spec = app.openapi(); print(json.dumps(spec, indent=2))" > openapi.json')
        return 1
    
    try:
        # Split the spec
        created_files = split_openapi()
        
        # Create README
        create_readme(Path("openapi_endpoints"))
        
        print("\n" + "=" * 60)
        print("✅ All done! Next steps:")
        print("=" * 60)
        print("1. Review files in openapi_endpoints/ directory")
        print("2. Upload individual files to watsonx Orchestrate Skills Catalog")
        print("3. Test each skill independently")
        print("4. See openapi_endpoints/README.md for detailed instructions")
        print("\n💡 Tip: Start with openapi_analyze_energy_post.json")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
