#!/bin/bash

while getopts "n:p:" opt; do
    case $opt in
        n) name+=("$OPTARG");;
        p) longs+=("$OPTARG");;
    esac
done
shift $((OPTIND -1))
declare -a shorts

# Pipe all echo also to file
exec 6>&1           # Link file descriptor #6 with stdout.
exec > ./${name}.sh

### Make the usage statement
# Using multiple echos instead of "cat <<EOT >> ./${name}.sh"
# because of buffer issues (text being written to file out of order)
echo "#!/bin/bash"
echo "### USAGE ######################################################################"
echo "read -r -d '' USAGE << ENDOFUSAGE"
echo "" 
echo "${name}.sh uses iptables to block the NFS ports from the hostnames listed in the configuration file. "
echo "This script actively writes the iptables. It does NOT save them (to persist past a reboot.) This is intentional to avoid accidental administrative lock-outs. "
echo ""
echo "  -h | --help "
echo "        Print this help statement."
count=0
for val in "${longs[@]}"; do
	shorts[$count]=${val:0:1}
	echo ""
	echo "  -${shorts[$count]} | --$val"
	echo "        Description."
	echo "        (DEFAULT: )"
    ((count++))
done
echo ""
echo "  -d | --dry-run"
echo "        Take no real action."
echo "        (DEFAULT: false)"
echo ""
echo "  -v | --verbose"
echo "        Verbose output."
echo "        (DEFAULT: false)"
echo ""
echo "ENDOFUSAGE"
echo "### USAGE ######################################################################" 

### Set the getops stuff
# Final command like...
# OPTS=`getopt -o hc:dv --longoptions help,config-file,dry-run,verbose: -n 'parse-options' -- "$@"`
echo "#--- SET GETOPTS --------------------------------------------------------------"

echo -n "OPTS=\`getopt -o h" # Set initial
#echo $command > ./${name}.sh 
# Do the short (single character) params first
for short in "${shorts[@]}"; do
	echo -n "${short}:"
done
echo -n "dv"
# Do the long versions next
echo -n " --longoptions help,"
for long in "${longs[@]}"; do
	echo -n "${long},"
done
# Delete the final trailing comma
#echo -en '\b'

# Finish the command
echo "dry-run,verbose: -n 'parse-options' -- \"\$@\"\`"

### The written script's check that the options were parsed
echo ""
echo "if [ $? != 0 ] ; then"
echo "    echo \"Failed parsing options.\" >&2"
echo "    echo \"$USAGE\" >&2"
echo "    exit 1"
echo "fi"
echo "# echo \"\$OPTS\""
echo "eval set -- \"\$OPTS\""
echo ""

### Written script's Set the defaults
echo "#--- SET DEFAULTS --------------------------------------------------------------"
for long in "${longs[@]}"; do
	long=${long//-}
	# Remove any dashes, but leave underscores
	echo "${long^^}=\"\""
done
echo "DRY_RUN=false"
echo "VERBOSE=false"

### Written script's run the getopts 
echo ""
echo "#--- RUN GETOPTS --------------------------------------------------------------"
echo "while true; do"
echo "  case \"\$1\" in"
echo "    -h | --help) echo \"\$USAGE\" >&2; shift ;;"
count=0
for val in "${longs[@]}"; do
	shorts[$count]=${val:0:1}
	variable=${val//-}
	echo "    -${shorts[$count]} | --${val}) ${variable^^}=\"\$2\"; shift; shift ;;"
    ((count++))
done
echo "    -d | --dry-run) DRY_RUN=true; shift ;;"
echo "    -v | --verbose) VERBOSE=true; shift ;;"
echo "    -- ) shift; break ;;"
echo "    * ) break ;;"
echo "  esac"
echo "done"

### Written script's Print verbose if set
echo ""
echo "if [ \${VERBOSE} == true ]; then"
for long in "${longs[@]}"; do
	long=${long//-}
	echo "    echo \"${long^^} = \$${long^^}\""
done
echo "fi"

## Written script's check for parameters
echo ""
echo "#--- PARAM MODS --------------------------------------------------------------"
echo "# [[ ! -f \${CONFIGFILE} ]] && { echo; echo \"Config file \${CONFIGFILE} does not appear to exist or is not readable. \"; exit 1; }"

### Written script's function placeholder
echo ""
echo "#--- FUNCTIONS --------------------------------------------------------------"
echo "function command() {"
echo "  if [ \${DRY_RUN} == true ] || [ \${VERBOSE} == true ]; then"
echo "    echo \"\$1\""
echo "  fi"
echo "  if [ \${DRY_RUN} != true ]; then"
echo "    eval \"\$1\""
echo "  fi"
echo "}"

### Written script's placehold for the main function
echo ""
echo "# MAIN() ---------------------------------------------------------------------"
echo "command \"ls -la\""

### Make the new script executable
chmod 700 ./${name}.sh
