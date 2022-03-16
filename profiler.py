"""
A script to debug performance bottlenecks uniformly
without the need to manually "eye-ball" the actions
"""
import maya.cmds as cmds

# Set the cache size of the profile. A value of 100 means to cache up to 100MB of data
buffer_size = 100

# The location where the data is saved to
#  profile_output =  "C:\Users\<user_name>\Documents\profile_test.txt")
profile_output =  "C:\Users\<user_name>\Documents\profile_test.txt")

# If the viewport is not needed for debugging, set this to False
refresh_viewport = True

# A series of actions to be profiled
def profile_steps():
    pass
	
# ================================================================================
if refresh_viewport:
    cmds.refresh(suspend = True)
cmds.profiler(bufferSize = buffer_size)
cmds.profiler(sampling = True)
profile_steps()
cmds.profiler(sampling = False)
cmds.profiler(output = profile_output)
cmds.profiler(load = profile_output)
if refresh_viewport:
    cmds.refresh(suspend = False)
