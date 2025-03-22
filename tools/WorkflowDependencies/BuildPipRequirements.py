import yaml

# Load the environment.yml file
with open("env.yaml", "r") as file:
    env_data = yaml.safe_load(file)

# Extract the pip packages
pip_packages = []
for dep in env_data.get("dependencies", []):
    if isinstance(dep, dict) and "pip" in dep:
        pip_packages.extend(dep["pip"])

# Write to requirements.txt
with open("requirements.txt", "w") as file:
    for package in pip_packages:
        file.write(f"{package}\n")

print("requirements.txt generated successfully.")
