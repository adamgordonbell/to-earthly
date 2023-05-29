Here's a bash script that recreates the steps of the build:

```bash
#!/bin/bash

# Step 1: Install Node.js version 19.x
curl -fsSL https://deb.nodesource.com/setup_19.x | sudo -E bash -
sudo apt-get install -y nodejs

# Step 2: Check if the cache exists for the current package-lock.json hash, if not, create it
PACKAGE_LOCK_HASH=$(sha1sum package-lock.json | awk '{ print $1 }')
CACHED_NODE_MODULES_DIR="/tmp/node_modules_cache/$PACKAGE_LOCK_HASH"

if [ -d "$CACHED_NODE_MODULES_DIR" ]; then
  echo "Using cached node_modules"
  cp -R "$CACHED_NODE_MODULES_DIR" ./node_modules
else
  echo "Cache not found, creating new cache"
  npm install
  mkdir -p "$CACHED_NODE_MODULES_DIR"
  cp -R ./node_modules "$CACHED_NODE_MODULES_DIR"
fi

# Step 3: Install npm dependencies
npm install

# Step 4: Run npm tests
npm test
```

Save this script as `build.sh` and make it executable with `chmod +x build.sh`. Then, you can run the script with `./build.sh` to perform the build steps.