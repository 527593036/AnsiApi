#!/bin/bash

filepath=$(cd `dirname $0`; pwd);cd $filepath
cat inventory.cache
