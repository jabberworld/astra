# /* encoding: utf-8 */
# Copyright sTools © simpleApps CodingTeam (Tue Oct 13 22:14:13 2011)
# This program published under GPL v3 license
# See LICENSE.GPL for more details

# OS.
import os

def getArchitecture():
	arch = os.uname()[4]
	return "[%s]" % arch
