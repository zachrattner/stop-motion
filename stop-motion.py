###############################################################################
# stop-motion.py
# Generate video files from sequences of images. Requires ffmpeg.
#
# Licensed under WTFPL: http://www.wtfpl.net/
#
# By Zach Rattner
# December 23, 2013
###############################################################################

#!/usr/bin/python

import sys, getopt, os

def main(argv):
  input_dir = ""
  type      = ""
  fps       = ""
  output    = ""

  # Attempt to parse command-line arguments
  try:
    opts, args = getopt.getopt(argv, "i:t:f:o:", 
                  ["in=", "type=", "fps=", "out="])
  except getopt.GetoptError:
    print_usage()
    sys.exit(2)
  
  # Import and validate parameters
  for opt, arg in opts:
    if opt in ("-i", "--in"):
      input_dir = arg
    if opt in ("-t", "--type"):
      type = arg
    elif opt in ("-f", "--fps"):
      fps = int(arg)
    elif opt in ("-o", "--out"):
      arg = "%s.mp4" % arg
      output = arg
      
  if not input_dir or not type or not fps or not output:
    print_usage()
    sys.exit()
  
  if not os.path.exists(input_dir):
    print "Input directory does not exist: ", input_dir
    sys.exit()
    
  if not os.path.isdir(input_dir):
    print "Input directory is not a folder: ", input_dir
    sys.exit()
    
  if os.path.exists(output):
    print "Output file already exists: ", output
    sys.exit()
    
  if os.access(output, os.W_OK):
    print "Output file not writable: ", output
    sys.exit()
      
  if fps < 1:
    print "Invalid duration: ", fps
    sys.exit()
  
  # Build command - options for quality are hd720 hd1080 2k 4k
  command = "ffmpeg -r %s -pattern_type glob -i '%s/*.%s' -s hd1080 %s" % (fps, input_dir, type, output)

  print "About to execute command:"
  print command
  print ""
  
  rsp = os.system(command)
  
  if rsp == 0:
    print "All done!"
  else:
    print "Finished with error code: ", rsp
  
def print_usage():
  print "Stop Motion - generate video files from images"
  print "stop-motion.py -i <input> -t <type> -f <fps> -o <output>"
  print "  -i --in    directory where input images are stored"
  print "  -t --type  file type, typically jpg or png"
  print "  -f --fps   frames (images) per second "
  print "  -o --out   output file name. mp4 will be appended"
      
if __name__ == "__main__":
  main(sys.argv[1:])