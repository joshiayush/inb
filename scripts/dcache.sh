#!/bin/bash

function dcache() {
  find "$ProjectRootDirectory/inb" -name "__pycache__" > pycache

  while IFS= read -r cache_file; do
    rm -r $cache_file
  done < pycache

  rm pycache
}