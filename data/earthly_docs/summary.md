Earthfiles are similar to Dockerfiles but are comprised of a series of target declarations and recipe definitions. They provide a rough structure that includes base-recipes, target-names, and command-names. Each recipe contains a series of commands.

## FROM

* `FROM <image-name>`
* `FROM [--platform <platform>] [--allow-privileged] <target-ref> [--<build-arg-key>=<build-arg-value>...]`

The FROM command in an Earthfile works like the FROM instruction in Dockerfile, but with added ability to use another target's image as the base image. The FROM ... AS ... form available in Dockerfile syntax is not supported in Earthfiles. Instead, developers can define a new Earthly target.

There are several options available within the FROM command in Earthfiles such as --<build-arg-key>=<build-arg-value>, --platform <platform>, and --allow-privileged. These options allow you to set value overrides for build args, specify the platform to build on, and allow remotely-referenced targets to request privileged capabilities respectively.

## RUN

* `RUN [--push] [--entrypoint] [--privileged] [--secret <env-var>=<secret-ref>] [--ssh] [--mount <mount-spec>] [--] <command>`

The RUN command is used in the Earthfile (analogous to Dockerfile) to execute commands in the build environment of the current target. It can be used in two forms, the exec form (without shell) and the shell form (with shell).

The command has several flags/options that allow for enhanced functionality such as --push (executes command only if all other instructions succeed), --entrypoint (uses current image entrypoint to prepend the command), --privileged (allows the command to use privileged capabilities), --secret (provides a secret to the command), --ssh (allows command to access the ssh authentication client), --mount (mounts a file or directory in the build environment), and --interactive (opens an interactive prompt during the target build).

The RUN command operates in a layered structure, meaning each command creates a new layer in the build environment. These layers are cached and can be reused in subsequent builds, unless the --no-cache flag is used. Special rules apply to the usage of the --interactive flag (e.g., it must be the last command and cannot be in a LOCALLY-designated target).

## COPY

* `COPY dir1 dir1`
* `COPY (+target1/artifact --arg1=foo --arg2=bar) ./dest/path`
* `COPY +dummy-target/encoded-data .`

Contextual Copying: The COPY command in Earthfiles allows the copying of files and directories from one context to another. It can operate in a classical form, copying from the build context into the build environment, or in an artifact form, copying artifacts from the environments of other build targets into the current one.

Build Arguments and Options: The COPY command supports build arguments and several options, such as --dir, which alters the behavior to copy directories themselves rather than their contents, and --<build-arg-key>=<build-arg-value>, allowing build arguments to be overridden. Other options include --keep-ts to maintain file creation timestamps, --keep-own to retain file ownership information, --if-exists to only copy if the source exists, and --platform to specify the platform for building the artifact.

Differences from Dockerfile: COPY in Earthfiles differs from Dockerfiles in a few key aspects. For instance, URL sources and absolute paths are not supported, and instead of the --from option, you can use a combination of SAVE ARTIFACT and COPY in the artifact form. Also, an .earthlyignore file can be used to exclude file patterns from the build context.

## ARG

* `ARG [--required] <name>[=<default-value>]` 
* `ARG [--required] <name>=$(<default-value-expr>)` 

ARG declares a variable with a name and an optional default value. If no default value is provided, an empty string is used. The scope of the variable is limited to the recipe of the current target or command and only from the point it is declared onward.

The value of an ARG can be overridden either from the earthly command or from another target, when implicitly or explicitly invoking the target containing the ARG.

An ARG can be marked as required with --required flag. A required ARG must be provided at build time and cannot have a default value. This can help eliminate cases where an ARG is unexpectedly set to "".

## SAVE ARTIFACT

* `SAVE ARTIFACT [--keep-ts] [--keep-own] [--if-exists] [--force] <src> [<artifact-dest-path>] [AS LOCAL <local-path>]`

Copying Artifacts: The SAVE ARTIFACT command copies files, directories, or series of files and directories from the build environment into the artifact environment. If AS LOCAL is also specified, the artifact will also be copied to the host at the specified location upon successful build completion.

Directory and File Distinction: When saving an artifact locally, a directory artifact will replace the destination entirely, while a file artifact will be copied into the destination directory. For example, SAVE ARTIFACT ./my-directory AS LOCAL ./destination will replace ./destination, but SAVE ARTIFACT ./my-directory/* AS LOCAL ./destination will merge the contents into ./destination.

Options to Consider: --keep-ts prevents overwriting of file creation timestamps; --keep-own keeps file ownership information; --if-exists ensures artifacts are saved only if they exist, ignoring the SAVE ARTIFACT command otherwise; --force allows potentially unsafe save operations, like writing to or overwriting a file outside of the Earthfile's context directory.

## SAVE IMAGE

* `SAVE IMAGE [--cache-from=<cache-image>] [--push] <image-name>...` 
* `SAVE IMAGE --cache-hint`

Image Saving and Naming: The SAVE IMAGE command in Earthly is used to mark the current build environment as an image of the target and assign it one or more output image names. This command can be used multiple times to assign different image names to the same build.

Pushing and Caching: The command supports options like --push and --cache-from, enabling the developer to push the image to an external registry or add additional cache sources. The --push option also allows the image to be used as a cache source if inline caching is enabled.

Explicit Caching: Using the --cache-hint option, the developer can instruct Earthly to include the current target as part of the explicit cache. This option can be used to optimize build time by caching certain targets.

## BUILD

* `BUILD [--platform <platform>] [--allow-privileged] <target-ref> [--<build-arg-name>=<build-arg-value>...]`

The BUILD command is used in Earthly to initiate the construction of a target specified by <target-ref>. This could involve building images, saving artifacts for local output, or issuing push commands, depending on the settings enabled.

The command allows for customization through various options such as --platform to specify the build platform, --allow-privileged for privileged operations, and --<build-arg-key>=<build-arg-value> to set override values for build arguments. Note that build arguments can be constant strings, expressions involving other build args, or dynamic expressions based on the output of a command executed in the context of the build environment.

## Tip: COPY and FROM

In Earthly, the FROM command in an Earthfile sets the base environment for a target. This environment includes all the artifacts and images created and saved in the target that the FROM command is pointing to.

So, if you have target1 and you're creating artifacts in it using SAVE ARTIFACT, and then you have target2 where you're saying FROM target1, the build environment of target2 automatically inherits all the artifacts from target1. You don't need to use the COPY command to transfer those artifacts from target1 to target2 - it's done automatically by the FROM command.

However, if you change the base image in target1, this can affect the artifacts saved in target1. If you still want to use these artifacts in target2 even after changing the base image in target1, that's when you would use the SAVE ARTIFACT command in target1 and the COPY command in target2.

In essence, SAVE ARTIFACT and COPY together provide a way to persist and transfer artifacts across targets when the base image changes. If the base image isn't changing, then simply using FROM is sufficient.

## Tip: COPY Directories

Use COPY --dir to copy multiple directories
The classical Dockerfile COPY command differs from the unix cp in that it will copy directory contents, not the directories themselves. This requires that copying multiple directories to be split across multiple lines:
```
# Avoid: too verbose
COPY dir-1 dir-1
COPY dir-2 dir-2
COPY dir-3 dir-3
```
This is repetitive and uses more cache layers than should be necessary.
Earthly introduces a setting, COPY --dir, which makes COPY behave more like cp and less like the Dockerfile COPY. The --dir flag can be used therefore to copy multiple directories in a single command:
```
# Good
COPY --dir dir-1 dir-2 dir-3 ./
```

## Tip: COPY consilidation

Don't write code like this:
```
  COPY package.json .
  COPY tsconfig.json .
  COPY tsconfig.node.json .
  COPY postcss.config.cjs .
  COPY tailwind.config.cjs .
  COPY vite.config.ts .
  COPY public/ ./public
  COPY index.html .
  COPY src/ ./src
`Snippet 2``:`

Instead, it is better to translate it to this form:
```
  COPY index.html package.json tsconfig.json tsconfig.node.json postcss.config.cjs tailwind.config.cjs vite.config.ts .
  COPY --dir public src .
```

In the first snippet, each COPY command copies a single file or directory, which results in 9 separate COPY commands.

In the second snippet, the first COPY command copies multiple individual files at once, and the second COPY command copies the entire 'public' and 'src' directories, effectively reducing the number of COPY commands to just 2.

The second version is a best practice.

Depending on the context, it could also be further condensed to use glob wildcards:

```
  COPY index.html *.json *.config.cjs vite.config.ts .
  COPY --dir public src .
```

If all files are needed this may be more stable in the future when more files are added.
