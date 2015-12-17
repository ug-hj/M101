#!/usr/bin/python

from __future__ import division, print_function
import os
import argparse


def main(jobname, nprocs, queue, pycode, cfgfile, cmdline_options):
    """
    """
    jobname = jobname.replace(" ", "_")
    # Construct string that will be written to the batch file
    textlist = ["#!/bin/tcsh -f",
                "#PBS -N " + jobname,
                "#PBS -l nodes=1:ppn=" + str(nprocs),
                "#PBS -q " + queue,
                "#PBS -o /home/moraes/qsub_logs/",
                "#PBS -j oe",
                "#PBS -S /bin/tcsh", "",
                "cd $PBS_O_WORKDIR",
                "source /etc/profile.d/modules.csh",
                "module load python/2.7.8", "",
                "echo Working directory is $PBS_O_WORKDIR",
                "echo Running on host `hostname`",
                "echo Time is `date`",
                "echo Directory is `pwd`",
                "echo This jobs runs on the following processors:",
                "echo `cat $PBS_NODEFILE`"]

    if cfgfile == "":
        textlist.append("python " + pycode + " " + cmdline_options + "\n")
    else:
        textlist.append("python " + pycode + " @" + cfgfile + " " + cmdline_options + "\n")

    batchtext = "\n".join(textlist)

    # Save string to new shell file
    filename = ("qsub_launcher_" + jobname + ".sh")
    with open(filename, 'w') as batch:
        batch.write(batchtext)
    # Launch qsub job and erase batch file
    os.system("qsub " + filename)
    os.system("sleep 1")
    os.system("rm " + filename)

    return None

#--------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=
    '''
    fixme

    fixme - fixme - fixme
    '''
    , fromfile_prefix_chars='@')

    parser.add_argument('--jobname',
                        default="job",
                        help="")
    parser.add_argument('--nprocs',
                        default=1,
			type=int,
                        help="Healpix output map resolution")
    parser.add_argument('--queue',
                        default='compute',
                        help="")
    parser.add_argument('--pycode',
                        required=True,
                        help="")
    parser.add_argument('--cfgfile',
                        default="",
                        help="")
    parser.add_argument('--cmdline_options',
                        default="",
                        help="")

    args = parser.parse_args()
    main(args.jobname, args.nprocs, args.queue, args.pycode, args.cfgfile,
         args.cmdline_options)
