#!/bin/csh -f

# TODO:
# Change this to install release, accept argument PRODUCTION or TEST
# if TEST, need to modify some lines to use different DB

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

# Maintainance remainder
echo
echo Maintainance mode: remember to change index.php to reflect messages
echo

# copy  copy permissions files into test dir
cd /u/group/clas/www/gemc/html/test
chmod g+w -R *

cd SubMit
cp ../../SubMit/*.txt .

echo done
echo



