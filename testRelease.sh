#!/bin/csh -f

set grepo = https://github.com/mit-mc-clas12


### SubMit/web_interface on the gemc server
set destination=/group/clas/www/gemc/html/test

set installDir=$destination
rm -rf $installDir ; mkdir -p  $installDir ;  cd $installDir
foreach repo (web_interface)
	if ( -d $repo) then
		cd $repo
		echo Updating $repo
		git pull
		git status -u
		cd ..
	else
		git clone $grepo/$repo.git
	endif
end
echo

### SubMit on the gemc server       
set installDir=$destination/SubMit

rm -rf $installDir ; mkdir -p  $installDir ;  cd $installDir
foreach repo (utils client)
	if ( -d $repo) then
		cd $repo
		echo Updating $repo
		git pull
		git status -u
		cd ..
	else
		git clone $grepo/$repo.git
	endif
end
echo

### SubMit on /group
set destination=/group/clas12/SubMit/test

set installDir=$destination/SubMit
rm -rf $installDir ; mkdir -p  $installDir ;  cd $installDir
foreach repo (utils server client)
	if ( -d $repo) then
		cd $repo
		echo Updating $repo
		git pull
		git status -u
		cd ..
	else
		git clone $grepo/$repo.git
	endif
end
echo

# copy indexMaintanance.php to index.php
echo
echo Maintainance mode: cp indexMaintanance.php index.php
echo
cd /u/group/clas/www/gemc/html/web_interface
cp indexMaintanance.php index.php
echo done
echo


