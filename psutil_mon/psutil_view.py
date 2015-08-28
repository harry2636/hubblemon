
#
# Hubblemon - Yet another general purpose system monitor
#
# Copyright 2015 NAVER Corp.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os, socket
import common.settings
import common.core
import data_loader

psutil_preset = []

cpu_filter = [['system', 'user'], ['irq', 'softirq'], 'idle', 'iowait', 'nice']
mem_filter = [['total', 'available', 'free', 'used'], 'percent']
swap_filter = [['total', 'used', 'free'], ['sin', 'sout'], 'percent']
disk_filter = [['read_bytes', 'write_bytes'], ['read_count', 'write_count'], ['read_time', 'write_time']]
net_filter = [['bytes_recv', 'bytes_sent'], ['packets_recv', 'packets_sent'], ['dropin', 'dropout'], ['errin', 'errout']]
resource_filter = [['tcp_open', 'fd', 'handle'], ['process', 'thread'], 'retransmit', 'ctx_switch']


def system_view_brief(path, title = ''):
	loader_list = []

	file_path = os.path.join(path, 'psutil_cpu')
	loader_list.append(common.core.loader(file_path, cpu_filter, 'cpu'))
	
	file_path = os.path.join(path, 'psutil_memory')
	loader_list.append(common.core.loader(file_path, mem_filter, 'memory'))

	file_path = os.path.join(path, 'psutil_swap')
	loader_list.append(common.core.loader(file_path, swap_filter, 'swap'))

	file_path = os.path.join(path, 'psutil_disk')
	loader_list.append(common.core.loader(file_path, disk_filter, 'disk'))
	
	file_path = os.path.join(path, 'psutil_net')
	loader_list.append(common.core.loader(file_path, net_filter, 'net'))

	file_path = os.path.join(path, 'psutil_resource')
	loader_list.append(common.core.loader(file_path, resource_filter, 'resource'))
		
	return loader_list


def system_view(path, item, title = ''):
	if item == 'brief':
		return system_view_brief(path, title)

	loader_file_list = []
	loader_list = []

	for file in sorted(os.listdir(path)):
		file_path = os.path.join(path, file)
		if os.path.isfile(file_path) and file.startswith('psutil_' + item):
			loader_file_list.append(file_path)

	filter = None
	if item == 'cpu':
		filter = cpu_filter
	elif item == 'memory':
		filter = mem_filter
	elif item == 'swap':
		filter = swap_filter
	elif item == 'disk':
		filter = disk_filter
	elif item == 'net':
		filter = net_filter
	elif item == 'resource':
		filter = resource_filter
		
	
	for loader_file in loader_file_list:
		loader_list.append(common.core.loader(loader_file, filter, os.path.basename(loader_file)[:-4]))

	return loader_list


