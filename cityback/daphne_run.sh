#!/bin/bash

daphne -p 8000 -b 0.0.0.0 cityback.asgi:application -v 3

