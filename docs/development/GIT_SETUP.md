# Git Setup Instructions

## 1. Install Git

1. Download Git for Windows:
   - Go to: https://git-scm.com/download/windows
   - Download the latest version for Windows

2. Run the installer:
   - Accept the license
   - Choose default installation location
   - Select components (use defaults)
   - Choose default editor (Notepad recommended for beginners)
   - Let Git decide the default branch name
   - Choose "Git from the command line and also from 3rd-party software"
   - Use OpenSSL library
   - Checkout Windows-style, commit Unix-style line endings
   - Use MinTTY
   - Default pull behavior: "Fast-forward or merge"
   - Use Git Credential Manager
   - Enable file system caching

3. Verify installation:
   - Open Command Prompt
   - Run: `git --version`
   - Should show installed version

## 2. Initial Git Setup

After installation, run these commands:

```bash
# Set your name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set default branch name
git config --global init.defaultBranch main
```

## 3. Repository Setup

Once Git is installed, run these commands in the project directory:

```bash
# Navigate to project directory
cd "S:/Dropbox/Scott Only Internal/Quant_Python_24/Basic_XLSX_PlusCalc_Restored_120424"

# Initialize repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Working state with documentation"

# Create 'working' tag
git tag -a v1.0-working-dec4 -m "Working state: December 4, 2023"
```

## 4. Verify Setup

Check repository status:
```bash
# Show status
git status

# Show commit history
git log

# Show tags
git tag -l
```

## 5. Future Git Usage

### Daily Operations
```bash
# Check status
git status

# Stage changes
git add .

# Commit changes
git commit -m "Description of changes"
```

### Creating Working State Tags
```bash
# After verifying working state
git tag -a v1.x-working-description -m "Working state: description"
```

### Reverting to Previous State
```bash
# List tags
git tag -l

# Revert to tag
git checkout v1.x-working-description
```

## 6. Best Practices

1. **Commit Messages**
   - Start with verb (Add, Fix, Update)
   - Be specific about what changed
   - Reference any fixed issues

2. **Working State Tags**
   - Create after major milestones
   - Include date in tag name
   - Add detailed message

3. **Before Committing**
   - Run test suite
   - Update documentation
   - Review changes (git diff)

4. **Regular Maintenance**
   - Commit frequently
   - Tag stable versions
   - Keep documentation updated
