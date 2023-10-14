### Profile of randomized_motif_search 5 iterations on n=20 len 198 strings, finding k=15 mers
### Generated with cProfile

        73614217 function calls (73614069 primitive calls) in 21.916 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
  1324800    3.128    0.000    5.562    0.000 indexing.py:1213(_is_scalar_access)
  1324800    2.811    0.000   20.116    0.000 indexing.py:1139(__getitem__)
  1324800    1.722    0.000    4.674    0.000 frame.py:3985(_get_value)
  1324800    1.338    0.000    4.422    0.000 indexing.py:2678(check_dict_or_set_indexers)
 17228033    1.327    0.000    1.327    0.000 {built-in method builtins.isinstance}
  2649600    1.047    0.000    2.710    0.000 {built-in method builtins.any}
  3974400    1.017    0.000    1.699    0.000 indexing.py:1144(<genexpr>)
    88320    0.725    0.000   21.075    0.000 lib.py:339(<listcomp>)
  3974400    0.697    0.000    0.947    0.000 indexing.py:1143(<genexpr>)
  2649600    0.683    0.000    0.683    0.000 frame.py:952(axes)
  3974400    0.682    0.000    0.874    0.000 indexing.py:2685(<genexpr>)
  1324800    0.652    0.000    1.185    0.000 base.py:3762(get_loc)
  1324800    0.617    0.000    0.961    0.000 frame.py:4405(_get_item_cache)
  3974400    0.607    0.000    0.789    0.000 indexing.py:2694(<genexpr>)
  2649600    0.562    0.000    0.693    0.000 base.py:6238(_index_as_unique)
  2649600    0.491    0.000    0.682    0.000 common.py:367(apply_if_callable)
  1324800    0.416    0.000    0.683    0.000 series.py:750(_values)
  1324800    0.400    0.000    0.400    0.000 {method 'get_loc' of 'pandas._libs.index.IndexEngine' objects}
    91582    0.335    0.000    0.335    0.000 {method 'reduce' of 'numpy.ufunc' objects}
  2649624    0.273    0.000    0.273    0.000 {pandas._libs.lib.is_scalar}
  1324800    0.267    0.000    0.267    0.000 managers.py:1960(internal_values)
  2649624    0.250    0.000    0.250    0.000 {pandas._libs.lib.is_iterator}
  1324800    0.234    0.000    0.234    0.000 indexing.py:289(loc)
  1325184    0.227    0.000    0.227    0.000 __init__.py:33(using_copy_on_write)
  1324800    0.218    0.000    0.218    0.000 generic.py:659(ndim)
  2649600    0.192    0.000    0.192    0.000 {built-in method builtins.callable}
      480    0.158    0.000   21.888    0.046 lib.py:329(profile_most_probable_kmer)
    91582    0.135    0.000    0.574    0.000 fromnumeric.py:71(_wrapreduction)
  1324800    0.133    0.000    0.133    0.000 base.py:6611(_maybe_cast_indexer)
  1324800    0.130    0.000    0.130    0.000 range.py:381(is_unique)
1326175/1326031    0.112    0.000    0.112    0.000 {built-in method builtins.len}
  1324824    0.109    0.000    0.109    0.000 {method 'get' of 'dict' objects}
    88320    0.077    0.000    0.642    0.000 fromnumeric.py:2979(prod)
    88608    0.052    0.000    0.052    0.000 {built-in method builtins.getattr}
    91582    0.043    0.000    0.043    0.000 fromnumeric.py:72(<dictcomp>)
    88320    0.012    0.000    0.012    0.000 fromnumeric.py:2974(_prod_dispatcher)
    91582    0.009    0.000    0.009    0.000 {method 'items' of 'dict' objects}
       53    0.008    0.000    0.020    0.000 lib.py:283(count_motif_matrix)
     3233    0.002    0.000    0.012    0.000 fromnumeric.py:2177(sum)
       53    0.001    0.000    0.001    0.000 {built-in method numpy.array}
      360    0.001    0.000    0.002    0.000 managers.py:991(iget)
     1440    0.001    0.000    0.001    0.000 generic.py:6206(__setattr__)
      360    0.001    0.000    0.001    0.000 generic.py:6147(__finalize__)
      384    0.001    0.000    0.001    0.000 generic.py:274(__init__)
       24    0.001    0.000   21.888    0.912 lib.py:395(<listcomp>)
      360    0.001    0.000    0.008    0.000 frame.py:3779(_ixs)
      360    0.001    0.000    0.004    0.000 frame.py:4387(_box_col_values)
        1    0.000    0.000   21.916   21.916 lib.py:372(randomized_motif_search)
       48    0.000    0.000    0.001    0.000 {pandas._libs.lib.maybe_convert_objects}
      720    0.000    0.000    0.001    0.000 range.py:973(__getitem__)
     3233    0.000    0.000    0.000    0.000 fromnumeric.py:2172(_sum_dispatcher)
       24    0.000    0.000    0.004    0.000 construction.py:237(ndarray_to_mgr)
       24    0.000    0.000    0.002    0.000 base.py:477(__new__)
       24    0.000    0.000    0.005    0.000 frame.py:668(__init__)
       53    0.000    0.000    0.000    0.000 numeric.py:136(ones)
      360    0.000    0.000    0.002    0.000 frame.py:656(_constructor_sliced_from_mgr)
      360    0.000    0.000    0.001    0.000 series.py:1372(_set_as_cached)
      360    0.000    0.000    0.000    0.000 range.py:409(get_loc)
       24    0.000    0.000    0.014    0.001 lib.py:297(profile_motif_matrix)
      360    0.000    0.000    0.001    0.000 generic.py:335(_from_mgr)
       24    0.000    0.000    0.001    0.000 construction.py:518(sanitize_array)
       29    0.000    0.000    0.012    0.000 lib.py:373(score)
      384    0.000    0.000    0.000    0.000 flags.py:53(__init__)
       24    0.000    0.000    0.001    0.000 base.py:841(_engine)
      360    0.000    0.000    0.000    0.000 blocks.py:1007(iget)
       24    0.000    0.000    0.001    0.000 base.py:2292(is_unique)
      125    0.000    0.000    0.000    0.000 {built-in method numpy.empty}
      360    0.000    0.000    0.000    0.000 flags.py:89(allows_duplicate_labels)
      360    0.000    0.000    0.001    0.000 frame.py:653(_sliced_from_mgr)
       24    0.000    0.000    0.000    0.000 managers.py:2042(create_block_manager_from_blocks)
       24    0.000    0.000    0.003    0.000 base.py:7512(ensure_index)
     1080    0.000    0.000    0.000    0.000 {pandas._libs.lib.is_integer}
      360    0.000    0.000    0.000    0.000 managers.py:1799(__init__)
       24    0.000    0.000    0.000    0.000 {method '_rebuild_blknos_and_blklocs' of 'pandas._libs.internals.BlockManager' objects}
       48    0.000    0.000    0.000    0.000 numeric.py:274(full)
       24    0.000    0.000    0.000    0.000 base.py:648(_simple_new)
      360    0.000    0.000    0.000    0.000 managers.py:169(blknos)
      360    0.000    0.000    0.000    0.000 {method 'index' of 'range' objects}
       24    0.000    0.000    0.000    0.000 cast.py:1147(maybe_infer_to_datetimelike)
       24    0.000    0.000    0.001    0.000 cast.py:119(maybe_convert_platform)
      720    0.000    0.000    0.000    0.000 generic.py:393(flags)
       24    0.000    0.000    0.000    0.000 blocks.py:2375(new_block_2d)
      100    0.000    0.000    0.000    0.000 random.py:292(randrange)
      360    0.000    0.000    0.000    0.000 managers.py:1902(_block)
      408    0.000    0.000    0.000    0.000 {built-in method __new__ of type object at 0x557327eef9a0}
      360    0.000    0.000    0.000    0.000 managers.py:185(blklocs)
       24    0.000    0.000    0.000    0.000 config.py:127(_get_single_key)
       24    0.000    0.000    0.000    0.000 {method 'add_index_reference' of 'pandas._libs.internals.BlockValuesRefs' objects}
       24    0.000    0.000    0.000    0.000 cast.py:1544(construct_1d_object_array_from_listlike)
      168    0.000    0.000    0.000    0.000 generic.py:37(_check)
       72    0.000    0.000    0.000    0.000 {built-in method _abc._abc_instancecheck}
       20    0.000    0.000    0.000    0.000 {method 'join' of 'str' objects}
       24    0.000    0.000    0.000    0.000 range.py:198(_simple_new)
      168    0.000    0.000    0.000    0.000 generic.py:42(_instancecheck)
       24    0.000    0.000    0.000    0.000 base.py:5152(_get_engine_target)
      360    0.000    0.000    0.000    0.000 generic.py:358(attrs)
      360    0.000    0.000    0.000    0.000 flags.py:57(allows_duplicate_labels)
       24    0.000    0.000    0.000    0.000 blocks.py:2346(get_block_type)
      100    0.000    0.000    0.000    0.000 random.py:239(_randbelow_with_getrandbits)
       24    0.000    0.000    0.000    0.000 common.py:137(is_object_dtype)
       24    0.000    0.000    0.003    0.000 construction.py:742(_get_axes)
       48    0.000    0.000    0.000    0.000 config.py:647(_get_deprecated_option)
       24    0.000    0.000    0.000    0.000 blocks.py:2317(maybe_coerce_values)
       24    0.000    0.000    0.000    0.000 config.py:145(_get_option)
       48    0.000    0.000    0.000    0.000 construction.py:484(ensure_wrapped_if_datetimelike)
       24    0.000    0.000    0.000    0.000 config.py:633(_get_root)
       24    0.000    0.000    0.000    0.000 api.py:379(default_index)
       24    0.000    0.000    0.000    0.000 config.py:271(__call__)
       24    0.000    0.000    0.000    0.000 base.py:69(shape)
       24    0.000    0.000    0.000    0.000 base.py:573(_ensure_array)
       24    0.000    0.000    0.000    0.000 construction.py:419(extract_array)
       24    0.000    0.000    0.000    0.000 managers.py:1734(_consolidate_check)
       24    0.000    0.000    0.000    0.000 common.py:1425(_is_dtype_type)
       48    0.000    0.000    0.000    0.000 {built-in method numpy.asarray}
       48    0.000    0.000    0.000    0.000 common.py:1322(is_ea_or_datetimelike_dtype)
       72    0.000    0.000    0.000    0.000 abc.py:117(__instancecheck__)
       96    0.000    0.000    0.000    0.000 range.py:963(__len__)
       24    0.000    0.000    0.000    0.000 base.py:7607(maybe_extract_name)
       24    0.000    0.000    0.000    0.000 {pandas._libs.lib.is_all_arraylike}
       24    0.000    0.000    0.000    0.000 base.py:458(_engine_type)
       24    0.000    0.000    0.000    0.000 config.py:686(_warn_if_deprecated)
       24    0.000    0.000    0.000    0.000 base.py:591(_dtype_to_subclass)
       24    0.000    0.000    0.000    0.000 construction.py:405(_check_values_indices_shape_match)
      100    0.000    0.000    0.000    0.000 random.py:366(randint)
       24    0.000    0.000    0.000    0.000 config.py:615(_select_options)
       24    0.000    0.000    0.000    0.000 construction.py:673(_sanitize_ndim)
       29    0.000    0.000    0.000    0.000 fromnumeric.py:2692(max)
       48    0.000    0.000    0.000    0.000 base.py:830(_reset_identity)
       24    0.000    0.000    0.000    0.000 managers.py:1726(is_consolidated)
       48    0.000    0.000    0.000    0.000 common.py:1255(is_1d_only_ea_dtype)
       24    0.000    0.000    0.000    0.000 __init__.py:43(using_pyarrow_string_dtype)
       24    0.000    0.000    0.000    0.000 construction.py:585(_ensure_2d)
       24    0.000    0.000    0.000    0.000 inference.py:334(is_hashable)
       24    0.000    0.000    0.000    0.000 construction.py:712(_sanitize_str_dtypes)
       72    0.000    0.000    0.000    0.000 base.py:71(<genexpr>)
       24    0.000    0.000    0.000    0.000 managers.py:1744(_consolidate_inplace)
       48    0.000    0.000    0.000    0.000 {pandas._libs.lib.is_list_like}
       24    0.000    0.000    0.000    0.000 common.py:1025(needs_i8_conversion)
      101    0.000    0.000    0.000    0.000 multiarray.py:1080(copyto)
       24    0.000    0.000    0.000    0.000 {method 'split' of 'str' objects}
      300    0.000    0.000    0.000    0.000 {built-in method _operator.index}
       48    0.000    0.000    0.000    0.000 base.py:908(__len__)
       24    0.000    0.000    0.000    0.000 common.py:121(classes)
       24    0.000    0.000    0.000    0.000 construction.py:665(_sanitize_non_ordered)
       24    0.000    0.000    0.000    0.000 construction.py:196(mgr_to_mgr)
       96    0.000    0.000    0.000    0.000 typing.py:1737(cast)
       24    0.000    0.000    0.000    0.000 config.py:674(_translate_key)
      135    0.000    0.000    0.000    0.000 {method 'getrandbits' of '_random.Random' objects}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.print}
       72    0.000    0.000    0.000    0.000 {built-in method builtins.issubclass}
       48    0.000    0.000    0.000    0.000 {pandas._libs.lib.is_np_dtype}
       72    0.000    0.000    0.000    0.000 base.py:5126(_values)
       24    0.000    0.000    0.000    0.000 managers.py:896(__init__)
        1    0.000    0.000    0.000    0.000 lib.py:409(<listcomp>)
      4/2    0.000    0.000    0.000    0.000 {built-in method _abc._abc_subclasscheck}
      100    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}
      100    0.000    0.000    0.000    0.000 {method 'bit_length' of 'int' objects}
       24    0.000    0.000    0.000    0.000 {built-in method builtins.hash}
       24    0.000    0.000    0.000    0.000 common.py:123(<lambda>)
       24    0.000    0.000    0.000    0.000 base.py:973(dtype)
       24    0.000    0.000    0.000    0.000 construction.py:732(_maybe_repeat)
       48    0.000    0.000    0.000    0.000 {built-in method builtins.hasattr}
       29    0.000    0.000    0.000    0.000 fromnumeric.py:2687(_max_dispatcher)
      4/2    0.000    0.000    0.000    0.000 abc.py:121(__subclasscheck__)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}