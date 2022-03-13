
import tensorflow as tf
import tensorflow_transform as tft

columns = ['pickup_community_area', 'fare', 'trip_start_month', 'trip_start_hour',
       'trip_start_day', 'trip_start_timestamp', 'pickup_latitude',
       'pickup_longitude', 'dropoff_latitude', 'dropoff_longitude',
       'trip_miles', 'pickup_census_tract', 'dropoff_census_tract',
       'payment_type', 'company', 'trip_seconds', 'dropoff_community_area',
       'tips']

_DENSE_FLOAT_FEATURE_KEYS = ['trip_miles', 'fare', 'trip_seconds']

_VOCAB_SIZE=10000
_OOV_SIZE =10

_BUCKET_FEATURE_KEYS = [
    'pickup_latitude', 'pickup_longitude', 'dropoff_latitude',
    'dropoff_longitude'
]

_BUCKET_SIZE = 10

_VOCAB_FEATURE_KEYS = [
    'payment_type',
    'company',
]

_LABEL_KEY = 'tips'
_FARE_KEY = 'fare'

def _transformed_name(key):
  return key + '_xf'

def _transformed_names(keys):
  return [_transformed_name(key) for key in keys]

def _fill_in_missing(x):
    """Replace missing values in a SparseTensor.
    Fills in missing values of `x` with '' or 0, and converts to a dense tensor.
    Args:
        x: A `SparseTensor` of rank 2.  Its dense shape should have size at most 1
        in the second dimension.
    Returns:
        A rank 1 tensor where missing values of `x` have been filled in.
    """
    default_value = '' if x.dtype == tf.string else 0
    return tf.squeeze(
        tf.sparse.to_dense(
            tf.SparseTensor(x.indices, x.values, [x.dense_shape[0], 1]),
            default_value
        ),
    )

def preprocessing_fn(input):
    output={}
    print(f"Appliing standardization on columns: {_DENSE_FLOAT_FEATURE_KEYS}")
    for key in _DENSE_FLOAT_FEATURE_KEYS:
        output[_transformed_name(key)] = tft.scale_to_z_score(
            _fill_in_missing(input[key]))

    print(f"Appliing vocabulary lookup on columns: {_VOCAB_FEATURE_KEYS}")
    for key in _VOCAB_FEATURE_KEYS:
        output[_transformed_name(key)] = tft.compute_and_apply_vocabulary(
            _fill_in_missing(input[key]),top_k =_VOCAB_SIZE, 
            oov_buckets = _OOV_SIZE)
    print(f"Appliing bucketization on columns: {_BUCKET_FEATURE_KEYS}")
    for key in _BUCKET_FEATURE_KEYS:
        output[_transformed_name(key)] = tft.bucketize(
            _fill_in_missing(input[key]),_BUCKET_SIZE)
        
    taxi_fare = _fill_in_missing(input[_FARE_KEY])
    tips = _fill_in_missing(input[_LABEL_KEY])

    output[_transformed_name(_LABEL_KEY)] = tf.where(
        tf.math.is_nan(taxi_fare),
        tf.cast(tf.zeros_like(taxi_fare), tf.int64),
        tf.cast(
            tf.greater(tips, tf.multiply(taxi_fare, tf.constant(0.10))),
            tf.int64),
        )
    return output
        
        
    
    


    





