project('MiSTeX', 'c', 'cpp')

cc = meson.get_compiler('c')

# defines to make packages happy. Seems we can't define these per library
#
# within lzma
add_global_arguments('-D_7ZIP_ST', language: 'c')

# flac
add_global_arguments(['-DPACKAGE_VERSION="1.3.3"', '-DFLAC_API_EXPORTS', '-DFLAC__HAS_OGG=0', 
  '-DHAVE_LROUND', '-DHAVE_STDINT_H', '-DHAVE_STDLIB_H', '-DHAVE_SYS_PARAM_H', 
  '-DENABLE_64_BIT_WORDS=0'], language: 'c')

# miniz
add_global_arguments(['-D_FILE_OFFSET_BITS=64', '-D_LARGEFILE64_SOURCE'], language: 'c')

date = run_command('date', '+"%y%m%d"', check: true)
add_global_arguments('-DVDATE=@0@'.format(date.stdout().strip()), language: ['c', 'cpp'])

add_global_arguments('-Wno-narrowing', language: ['c', 'cpp'])

# generate binary objects from binary png
mkbin = find_program('mkbinary.py')
ld = cc.cmd_array()[0]
png = generator(mkbin, 
  output: '@BASENAME@.o',
  arguments: ['@OUTPUT@', '@INPUT@', ld, target_machine.cpu_family()])

m_dep = cc.find_library('m', required: false)
z_dep = dependency('zlib', version: '>=1.2.8')
gpio_dep = cc.find_library('gpiod', required: true)
bluetooth_dep = cc.find_library('bluetooth', required: true)
imlib_dep = cc.find_library('Imlib2', required: true)

libco_inc = include_directories('lib/libco')
libco = library('libco',
  'lib/libco/arm.c',
  include_directories: libco_inc)
miniz_inc = include_directories('lib/miniz')
miniz = library('miniz',
  'lib/miniz/miniz.c',
  include_directories: miniz_inc)
md5_inc = include_directories('lib/md5')
md5 = library('md5',
  'lib/md5/md5.c',
  include_directories: md5_inc)
lzma_inc = include_directories('lib/lzma')
lzma = library('lzma',
  'lib/lzma/Alloc.c', 'lib/lzma/CpuArch.c', 'lib/lzma/Delta.c', 
  'lib/lzma/LzFind.c', 'lib/lzma/LzmaDec.c', 'lib/lzma/LzmaEnc.c',
  'lib/lzma/LzmaLib.c', 'lib/lzma/Sort.c',
  include_directories: lzma_inc)
flac_inc = include_directories('lib/flac/include', 'lib/flac/src/include')
flac = library('flac',
  'lib/flac/src/bitmath.c', 'lib/flac/src/bitreader.c', 'lib/flac/src/bitwriter.c',
  'lib/flac/src/cpu.c', 'lib/flac/src/crc.c', 'lib/flac/src/fixed.c', 'lib/flac/src/float.c',
  'lib/flac/src/format.c', 'lib/flac/src/lpc.c', 'lib/flac/src/md5.c', 'lib/flac/src/memory.c',
  'lib/flac/src/metadata_iterators.c', 'lib/flac/src/metadata_object.c', 'lib/flac/src/stream_decoder.c',
  'lib/flac/src/stream_encoder.c', 'lib/flac/src/stream_encoder_framing.c', 'lib/flac/src/window.c',
  dependencies: m_dep,
  include_directories: flac_inc)
chdr_inc = include_directories('lib/libchdr/include')
chdr = library('chdr', 
  'lib/libchdr/libchdr_bitstream.c', 'lib/libchdr/libchdr_cdrom.c', 
  'lib/libchdr/libchdr_chd.c', 'lib/libchdr/libchdr_flac.c',
  'lib/libchdr/libchdr_huffman.c',
  link_with: [flac, lzma, miniz],
  include_directories: [miniz_inc, chdr_inc, flac_inc, lzma_inc])
bt_inc = include_directories('lib/bluetooth')

logo_src = png.process('logo.png')

inc = [
  libco_inc, miniz_inc, md5_inc,
  lzma_inc, chdr_inc,
  flac_inc, bt_inc
]
support = ['support/arcade/buffer.cpp', 'support/arcade/mra_loader.cpp', 'support/archie/archie.cpp',
  'support/c64/c64.cpp', 'support/chd/mister_chd.cpp', 'support/megacd/megacd.cpp', 
  'support/megacd/megacdd.cpp', 'support/minimig/minimig_boot.cpp', 'support/minimig/minimig_config.cpp',
  'support/minimig/minimig_fdd.cpp', 'support/minimig/minimig_hdd.cpp', 'support/minimig/minimig_share.cpp',
  'support/neogeo/neogeo_loader.cpp', 'support/pcecd/pcecd.cpp', 'support/pcecd/pcecdd.cpp',
  'support/pcecd/seektime.cpp',
  'support/psx/psx.cpp', 'support/saturn/saturncdd.cpp', 'support/saturn/saturn.cpp', 
  'support/sharpmz/sharpmz.cpp', 'support/snes/snes.cpp', 'support/st/st_tos.cpp', 
  'support/uef/uef_reader.cpp', 'support/x86/x86.cpp', 'support/x86/x86_share.cpp']
src = ['audio.cpp', 'battery.cpp', 'bootcore.cpp', 'brightness.cpp',
  'cfg.cpp', 'charrom.cpp', 'cheats.cpp', 'DiskImage.cpp',
  'file_io.cpp', 'fpga_io.cpp', 'gamecontroller_db.cpp',
  'hardware.cpp', 'ide_cdrom.cpp', 'ide.cpp', 'input.cpp',
  'joymapping.cpp', 'menu.cpp', 'offload.cpp', 'osd.cpp',
  'profiling.cpp', 'recent.cpp', 'scaler.cpp', 'shmem.cpp',
  'smbus.cpp', 'spi.cpp', 'str_util.cpp', 'sxmlc.c', 
  'user_io.cpp', 'video.cpp', 'main.cpp']
executable('MiSTeX', 
  src,
  support,
  logo_src,
  include_directories: inc,
  dependencies: [z_dep, gpio_dep, bluetooth_dep, imlib_dep],
  link_with: [libco, miniz, md5, lzma, flac, chdr])
