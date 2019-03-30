"""
module::params
Store parameters for the application in this file.
If we do this, parameters for the application can 
be referenced with 

import params as p

p.params['my_param_name']
"""

"""
data::params
The global parameter dictionary
"""
params = dict()

"""
data::ALPHA
A small number representing the degree of parallelism in network calls
"""
ALPHA = 'alpha'

"""
data::B
B is the size in bits of the keys used to identify nodes and store and retrieve
data; in basic Kademlia this is 160, the length of an SHA1 digest (hash).
"""
B = 'B'
"""
data::K
k is the maximum number of contacts stored in a bucket; this is normally 20.
"""
K = 'k'

"""
data::T_EXPIRE
tExpire: the time in seconds after which a key/value pair expires; this is a time-to-live (TTL)
from the original publication date
"""
T_EXPIRE = 'tExpire'
"""
data::T_REFRESH
tRefresh: the time in seconds after which an otherwise unaccessed bucket must be refreshed
"""
T_REFRESH = 'tRefresh'
"""
data::T_REPLICATE
tReplicate: the interval in seconds between Kademlia replication events, when a node is
required to publish its entire database
"""
T_REPLICATE = 'tReplicate'
"""
data::T_REPUBLISH
tRepublish: the time in seconds after which the original publisher must republish
a key/value pair.
NOTE: The fact that tRepublish and tExpire are equal introduces a race
condition. The STORE for the data being published may arrive at the node just
after it has been expired, so that it will actually be necessary to put the
data on the wire. A sensible implementation would have tExpire significantly
longer than tRepublish. Experience suggests that tExpire=86410 would be
sufficient. 
"""
T_REPUBLISH = 'tRepublish'

"""
data::P_TIMEOUT
pTimeout: the time in seconds that a node waits before timing out on a connection
"""
P_TIMEOUT = 'pTimeout'

# No need to do the multi-threaded 'node discover' thing yet
params[ALPHA] = 1
# Set this to 16 so that we can actually tractibly think about it at first
params[B] = 16
# set k to a small number at first so its easier to analyze
params[K] = 4

# Use smaller values for time parameters to keep things tangible
params[T_EXPIRE] = 128 # 86400 in the lit
params[T_REFRESH] = 64 # 3600 in the lit
params[T_REPLICATE] = 64 # 3600 in the lit
params[T_REPUBLISH] = 256 # 86410 in the lit
params[P_TIMEOUT] = 3

