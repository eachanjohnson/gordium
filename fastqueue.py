# import things we need
from __future__ import division
import multiprocessing as mp
import io

# define global constants
_converter_dict = {key: value for key, value in zip(list('ATCG'), list('TAGC'))}

# define functions
def _complement_converter(letter):
    return _converter_dict[letter]

# define classes
class FastQLine(object):

    def __init__(self, line):
        self.line = line


class Seq(FastQLine):

    def __init__(self, seq):
        FastQLine.__init__(self, seq)
        self.seq = self.line.upper()
        self._converter_dict = {key: value for key, value in zip(list('ATCG'), list('TAGC'))}

    def reverse(self):
        return self.seq[::-1]

    def complement(self):
        return ''.join([self._converter_dict[letter] for letter in self.seq])

    def complement_parallel(self, pool_size=8):
        pool = mp.Pool(pool_size)

        complement = pool.map(_complement_converter, list(self.seq))

        return ''.join(complement)

    def reverse_complement(self):
        return ''.join([self._converter_dict[letter] for letter in self.seq[::-1]])

    def reverse_complement_parallel(self, pool_size=8):
        pool = mp.Pool(pool_size)

        complement = pool.map(_complement_converter, list(self.seq[::-1]))

        return ''.join(complement)


class SeqRead(object):

    '''Abstraction of a sequencing read'''

    def __init__(self, meta, seq, junk, qual, n, source):

        if n == -1 or 0 not in {len(_) for _ in [meta, seq, junk, qual, source]}:
            self.seq = seq
            self.meta = meta
            self.qual = qual
            self.junk = junk
            self.n = n
            self.source = source
        else:
            raise ValueError

    def chunk(self):
        return ''.join([self.meta, self.seq, self.junk, self.qual])

    def __str__(self):
        s = '{}: read number {}\n'.format(self.source, self.n)
        s += ''.join([self.meta, self.seq, self.junk, self.qual])
        return s


class FastQStream(object):

    def __init__(self, filenames, size):
        '''Abstraction of a FASTQ file stream that is sequencing read-aware'''
        import itertools
        self.filenames = filenames
        self.f = itertools.izip(*[open(filename, 'rU') for filename in self.filenames])
        self.fastq_buffer = []
        self.max_size = size
        self.buffer_size = 0
        self.line_number = -1
        self.read_number = -1
        self.current_line = ['' for _ in self.filenames]
        self.current_read = [SeqRead(meta='', seq='', junk='', qual='', n=self.read_number, source=filename) for
                             filename in self.filenames]

    def reinitialize(self):
        self.__init__(filenames=self.filenames, size=self.max_size)
        return self

    def fill_buffer(self):

        self.buffer_size = len(self.fastq_buffer)
        self.current_read = self.next_read()

        while self.buffer_size < self.max_size + 1 and self.current_read is not None:
            self.fastq_buffer.append(self.current_read)
            self.buffer_size += 1
            self.current_read = self.next_read()

        if self.current_read is None:
            return False
        else:
            return True

    def next_line(self):
        self.current_line = self.f.next()
        self.line_number += 1
        return self.current_line

    def next_read(self):
        self.read_number += 1
        try:
            meta = self.next_line()
            seq = self.next_line()
            junk = self.next_line()
            qual = self.next_line()
        except StopIteration:
            print('Reached end of file.')
            return None
        else:
            self.current_read = [SeqRead(
                meta=value,
                seq=seq[n],
                junk=junk[n],
                qual=qual[n],
                n=self.read_number,
                source=self.filenames[n]
            ) for n, value in enumerate(meta)]
            return self.current_read


class GeneratorFastQStream(object):

    def __init__(self, filenames):
        '''Abstraction of a FASTQ file stream that is sequencing read-aware. Based on generators.'''
        import itertools
        self.filenames = filenames
        self.f = itertools.izip(*[open(filename, 'rU') for filename in self.filenames])
        self.line_number = -1
        self.read_number = -1
        self.current_line = ['' for _ in self.filenames]
        self.current_read = [SeqRead(meta='', seq='', junk='', qual='', n=self.read_number, source=filename) for
                             filename in self.filenames]

    def reinitialize(self):
        self.__init__(filenames=self.filenames)
        return self

    def stream_files(self):
        """
        Use this as an iterator.
        :return:
        """
        m, s, j, q = '', '', '', ''

        for n, reads in enumerate(self.f):
            modulus = n % 4
            if modulus == 0:
                m = reads
            elif modulus == 1:
                s = reads
            elif modulus == 2:
                j = reads
            elif modulus == 3:
                q = reads
                self.read_number += 1

                self.current_read = [
                    SeqRead(meta=meta, seq=seq, junk=junk, qual=qual, n=self.read_number, source=filename) for
                                 meta, seq, junk, qual, filename in zip(m, s, j, q, self.filenames)
                ]
                yield self.current_read
