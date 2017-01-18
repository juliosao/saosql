# saosql
Lightweight graphical mysql client

## Install
Execute this command as root:
`make install

Its possible to install saosql in a diferent root folder with the PREFIX option
`make install PREFIX=rootfolder

## Generate RPM package
Execute this command to make a RPM in your rpmbuild folder (noarch)
`make rpm

## Generate DEB package
Execute this command to make a DEB package in the current directory
`make deb

## Generate a tar.bz2 package
Its possible to make a tar.bz2 with the programm to install in systems without rpm or dpkg using this command
`make dist
