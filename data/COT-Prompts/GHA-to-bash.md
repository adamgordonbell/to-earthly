First Prompt:
```
Given a GitHub Actions workflow YAML file, summarize how you would recreate the steps of this build using bash and docker.

The implementation will consist of a run.sh script that creates and runs a Docker container where our build.sh script is executed. This approach encapsulates our build process in a controlled environment (the Docker container), isolating it from the host machine and ensuring that it has all the necessary dependencies, regardless of where or on what machine the build is running. This is why we choose to use Docker and why we run the build process inside a Docker container, even though it may seem like overkill for  some simple build processes.

You will create three files:
* `run.sh`: A bash file that wraps docker. It will call docker build and afterward run steps like docker push. Steps like git cloning and changing into the repo aren't needed because this file is stored in the git repository along with the code.
* `build.Dockerfile`: A dockerfile with the correct base image to support the build steps. This includes any programming language tool and any dependencies needed for `build.sh`. 
* `build.sh` A bash file that runs the steps of the build process. It will run inside `build.Dockerfile` in the working directory of the repository. 

Other files will exist in the repository. Code files and other assets and possibly an application Dockerfile. Call that `app`.

Important considerations:
* no need to install dependencies, nor check out the code in `build.sh`because it is run inside the image produced from `build.Dockerfile`. Call that docker image `build`.
* `build.Dockerfile` should work without volume mounting. Files that are needed need to be copied in. 
* References to building/tagging and pushing a Docker image or container in GitHub Actions workflow YAML do not refer to `build.Dockerfile` and `build` but to the application `app` Dockerfile called `Dockerfile`. 
* Any pushing and tagging of images should be of images made from  app `Dockerfile` and not from `build.Dockerfile`. Docker image `build` is used strictly for building steps and is used as a way to set up dependencies for that build in a repeatable way. 
* Don't include any steps that executing the git hub action wouldn't produce. This may mean a step does nothing. 
* You do not need to mention chmod of `build.sh` or `run.sh`. That is taken care of.

{{yaml}}

Do not produce the files. Instead, describe how you would approach this problem. Then go through the yaml document section by section and discuss if steps should be included or omitted, which of the three files it should be in, and how it needs to be adapted to the new format.
```
Second Prompt:
````
Ok, produce the files. Remember`build.Dockerfile` should work without volume mounting. Files that are needed need to be copied in. 
```



        {{#user~}}
        Ok, produce the files. Remember`build.Dockerfile` should work without volume mounting. Files that are needed need to be copied in. 
        {{~/user}}
        {{#assistant~}}
        `run.sh`:
        ```
        {{gen "run.sh" temperature=0 max_tokens=500}}
        ```
       `build.Dockerfile`:
        ```
        {{gen "build.Dockerfile" temperature=0 max_tokens=500}}
        ``` 
        `build.sh`:
        ```
        {{gen "build.sh" temperature=0 max_tokens=500}}
        ``` 
        {{~/assistant}}  