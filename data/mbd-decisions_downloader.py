import kagglehub

# Download latest version
path = kagglehub.dataset_download("berndhe/mba-decisions")

print("Path to dataset files:", path)