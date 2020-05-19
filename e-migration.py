# The MIT License
#
#  Copyright 2020 UB Dortmund <daten.ub@tu-dortmund.de>.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

import logging
import timeit
from functools import partial
from logging.handlers import RotatingFileHandler
import subprocess
from multiprocessing import Pool
from os import listdir
from os.path import isfile, join
from pathlib import Path

import cleanup
import config

from marcxml_splitter import xml_splitter


# init logger
log_formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")

logger = logging.getLogger("e-migration log")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(config.LOG_FILE, maxBytes=1000000, backupCount=1)
handler.setFormatter(log_formatter)

logger.addHandler(handler)


def split_sources(source_dir='', target_dir=''):

    start = timeit.default_timer()

    # split SOURCE FILES
    files = [f for f in listdir(source_dir) if isfile(join(source_dir, f))]

    for file in files:

        try:
            # split XML file
            xml_splitter(source_dir=source_dir, filename=file, namespace='mx', target_dir=target_dir, size=config.PART_SIZE)

        except Exception as e:
            logger.error(e)

    stop = timeit.default_timer()
    duration = stop - start
    logger.info('duration of splitting the source data: %s' % duration)


def build_id_map(source_dir, files, marker):

    id_map = {}

    for file in files:
        with open('%s/%s' % (source_dir, file), 'r') as f:
            for line in f:
                id_map[line.strip()] = marker

    return id_map


def flux_starter(flux_start_script='', flux_file='', params=None):
    """ start Metafacture flux process """

    command = [flux_start_script, flux_file]
    if params:
        command += params

    #print(command)
    logger.info(command)

    # start flux process
    result = subprocess.run(command, stdout=subprocess.PIPE)
    ostr = result.stdout.decode('utf-8')
    #print(ostr)
    logger.info('%s: %s' % (command, ostr))


def metafacture_process(file='', source_dir='', target_dir=''):

    cleanup.cleanup_dir(data_dir=target_dir)

    params = ["morphDir=%s" % config.METAFACTURE_PROJECTS_DIR,
              "sourceFile=%s/%s" % (source_dir, file),
              "targetFile=%s/%s" % (target_dir, file),
              "id_map=%s/exclude_ids.map.tsv" % config.ID_MAP_DIR]
    flux_starter(flux_start_script=config.FLUX_START_SCRIPT,
                 flux_file='%s/e-migration.flux' % config.METAFACTURE_PROJECTS_DIR, params=params)

    return '[%s] metafacture_process: done' % file


if __name__ == '__main__':

    start = timeit.default_timer()

    # create tmp source dir
    Path(config.TMP_SOURCES_DIR).mkdir(parents=True, exist_ok=True)
    # split origin to parts
    split_sources(source_dir=config.SOURCES_DIR, target_dir=config.TMP_SOURCES_DIR)

    # collect id lists and build an id map with id as key and marker as value
    id_map = {}
    id_files = [f for f in listdir('%s' % config.NZEXCLUDE_DIR) if isfile(join('%s' % config.NZEXCLUDE_DIR, f))]
    id_map = {**id_map, **build_id_map(source_dir=config.NZEXCLUDE_DIR, files=id_files, marker='NZ')}
    id_files = [f for f in listdir('%s' % config.IZEXCLUDE_DIR) if isfile(join('%s' % config.IZEXCLUDE_DIR, f))]
    id_map = {**id_map, **build_id_map(source_dir=config.IZEXCLUDE_DIR, files=id_files, marker='IZ')}

    # write id map as TSV file
    Path(config.ID_MAP_DIR).mkdir(parents=True, exist_ok=True)
    with open('%s/exclude_ids.map.tsv' % config.ID_MAP_DIR, 'w') as f:
        for key in id_map.keys():
            f.write('%s\t%s\n' % (key, id_map[key]))

    stop = timeit.default_timer()
    duration = stop - start
    logger.info('duration preprocessing: %s' % duration)

    # do enrichment
    start = timeit.default_timer()

    source_files = [f for f in listdir('%s' % config.TMP_SOURCES_DIR) if isfile(join('%s' % config.TMP_SOURCES_DIR, f))]
    print(source_files)

    Path(config.RESULTS_DIR).mkdir(parents=True, exist_ok=True)
    with Pool(processes=config.NUMBER_OF_WORKERS) as pool:
        message = pool.map(partial(metafacture_process, source_dir=config.TMP_SOURCES_DIR, target_dir=config.RESULTS_DIR), source_files)
        logger.info(message)

    stop = timeit.default_timer()
    duration = stop - start
    logger.info('duration metafacture process: %s' % duration)

    # TODO validate files against MARCXML XSD
