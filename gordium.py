from __future__ import division
import tables
import fastqueue
import docopt
import os.path
import time

__author__ = 'Eachan Johnson'
__version__ = 0.1

__doc__ = '''
Usage:  gordium.py [-h|-v]
        gordium.py -d <demultiplex-params> (-r <read-files>...) (-b <barcode-files>...)

Options:
--help, -h                                              Show this page and exit
--version, -v                                           Show version number and exit
-d                                                      TSV of barcode values and filenames
-r <read-files>..., --reads <read-files>...             List of files containing reads
-b <barcode-files>..., --barcodes <barcode-files>...    List of files containing barcodes to be matched
'''

# functions
def println(text):

    print('{} > {}'.format(time.ctime(), text))

    return None


# classes


# main function

def main():

    println('{}\'s demultiplexer version {}'.format(__author__, __version__))

    args = docopt.docopt(__doc__, version=__version__)

    #print args
    println('Reading demultiplexing params file {}...'.format(args['<demultiplex-params>']))
    params_table = tables.Table().from_tsv(args['<demultiplex-params>'])

    n_read_files = len(args['--reads'])
    #read_file_indices = range(n_read_files)
    n_barcode_files = len(args['--barcodes'])
    #barcode_file_indices = range(n_read_files, n_read_files + n_barcode_files)

    #print read_file_indices, barcode_file_indices]

    suffices = [suffix + 1 for suffix in range(n_read_files)] + \
               ['barcode_{}'.format(str(suffix + 1)) for suffix in range(n_barcode_files)]

    seq_routing_dict = {tuple(row[barcode_header.upper()] for barcode_header in suffices[n_read_files:n_read_files + n_barcode_files]
                              if barcode_header.upper() in row):
                            tuple(open('{}.{}.fastq'.format(os.path.basename(row['OUTPUT_PREFIX']), suffix), 'w')
                                  for suffix in suffices)
                        for row in params_table.rows()}

    for barcode_tuple in seq_routing_dict:
        println('Barcodes {} are routed to {}'.format(' '.join(list(barcode_tuple)),
                                                      ', '.join([output_file.name for output_file in
                                                                 seq_routing_dict[barcode_tuple]])))

    #print seq_routing_dict
    println('Setting up FASTQ file stream with {}...'.format(', '.join(args['--reads'] + args['--barcodes'])))
    fastq_stream = fastqueue.GeneratorFastQStream(args['--reads'] + args['--barcodes'])

    println('Demultiplexing...')
    for reads in fastq_stream.stream_files():

        barcodes = tuple(read.seq.rstrip() for read in reads[n_read_files:n_read_files + n_barcode_files])

        try:

            output_files = seq_routing_dict[barcodes]

        except KeyError:

            output_files = seq_routing_dict[('N', 'N')]

        for n, read in enumerate(reads):

            output_files[n].write(read.chunk())


    println('Closing files...')
    for barcode_tuple in seq_routing_dict:

        for output_file in seq_routing_dict[barcode_tuple]:

            output_file.close()

    #for read in fastq_stream.stream_files():


    #for row in params_table.rows():

    println('Done!')

    return 0


# boilerplate
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        println('!!! Keyboard interrupt: Quitting')
        quit()