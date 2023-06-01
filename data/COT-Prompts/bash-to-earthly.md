First Prompt:
```
You are creating an Earthfile from several bash and dockerfiles. I'll share Earthly documentation with you and then describe the conversion process. 
{{Earthly tutorial}}

The tutorial is over. I will now describe the task. But first, say ok. And I will proceed.
```

Second Prompt:
```
You are creating an Earthfile from the following inputs. 
*  `Files`: A Description of the file structure of the project. Use the file structure to determine what files need to be copied in at each stage of the docker multi-stage build. 
* `run.sh`: A bash file that wraps docker. It will call docker build and afterward run steps like docker push. 
* `build.Dockerfile`: A dockerfile with the correct base image to support the build steps. This should become the `base` and possibly the `deps` steps in the docker file.
* `build.sh` A bash file that runs the build steps. These steps should become targets in the Earthfile. 
`Files:`
`run.sh`:
build.Dockerfile
`build.sh`:


