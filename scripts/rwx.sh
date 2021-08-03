#!/bin/bash

#!/bin/bash

function rwx() {
  # @brief Changes the filemodes of the files present in the
  # ProjectRootDirectory
  # @param 1 String containing the owners
  # @param 2 String that tells whether to grant or revoke
  # permission (+|-)
  # @param 3 String containing the file modes

  # Change file mode of the files/directories and sub-directories
  # present in the ProjectRootDirectory
  chmod $1$2$3 -R "$ProjectRootDirectory/inb/" "$ProjectRootDirectory/scripts/"

  # Set git config core.filemode to false to tell git not to track
  # the access bits of the files/directories present in this project
  git config core.filemode false
}