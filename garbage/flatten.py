

#
# TODO: more tests
#
def flatten_dict(d):
    ''' flatten_dict

    Return plain list of tuples with concatinated paths to leafs.

    '''
    result = []

    if not (d and isinstance(d, dict)):
        return result

    node_stack = [([k], v) for k, v in d.iteritems()]

    while node_stack:
        path, item = node_stack.pop()

        if item and isinstance(item, dict):
            node_stack.extend([(path + [k], v) for k, v in item.iteritems()])
        else:
            result.append(('.'.join(path), item))

    return result


#
# Note: not tested at all!
#
def flatten_dict_rec(d):

    def flatten_dict_rec_impl(d, current_path, result):
        if not (d and isinstance(d, dict)):
            return

        for k, v in d.iteritems():
            if v and isinstance(v, dict):
                new_path = []
                new_path.extend(current_path)
                new_path.append(k)

                flatten_dict_rec_impl(v, new_path, result)
            else:
                result.append(('.'.join(current_path + [k]), v))

    current_path = []
    result = []

    flatten_dict_rec_impl(d, current_path, result)

    return result


d = dict(a=1,b=2,c=dict(z=100,x=500,y=60,d=dict(q=42)), d=dict(r=dict()))

print 'result(s) for d = {}'.format(d)

result_rec = flatten_dict_rec(d)
result_rec
print '   rec: \t{}'.format(result_rec)

result = flatten_dict(d)
result.sort()
print 'nonrec: \t{}'.format(result)

print dict(result_rec) == dict(result)
