# Autogen Experiments

## Overview

Repository for experiments for [Autogen](https://github.com/microsoft/autogen) by Microsoft. This is an interesting approach to working with LLMs using user proxies, it can also do group chats with multiple experts and works with functions. This repo has a working implementation with some work done to incorporate llama index, which is slightly redundant because autogen supplies it's own document retrevial solution, but I needed to interface with some existing technology. I am also doing basic experiments with the perplexity AI API.

## Setup

build docker image

```bash
docker build -t autogen_experiments . --no-cache
# -t used to name and optionally a tag in the 'name:tag' format your image
```

use docker-compose

```bash
docker up
```

### or you can run docker

```bash
docker run --env-file .env -v $(pwd):/app autogen_experiments
# This command runs a Docker container from the `autogen_experiments` image, loads environment variables from a file named `.env`, and mounts the current directory to `/app` inside the container.
```

```bash
docker run --rm --env-file .env -v $(pwd):/app autogen_experiments

# Using `--rm` Flag**: Include the `--rm` flag in your `docker run` command to automatically remove the container when it exits:
```

### configure environment variables

look at `env.example` and `OAI_CONFIG_LIST.example`` for examples of how to configure the environment variables, replace the example values with your own, remove the `.example` from the file name and you should be good to go.

## important files

Update text files in `app/resources` to change the input data for the experiments.

`app/resources/chat_message.md` is the main test message
