import numpy as np
import json

from sklearn.preprocessing import MinMaxScaler


def pad(FTCP, pad_width):
    '''
    This function zero pads (to the end of) the FTCP representation along the second dimension

    Parameters
    ----------
    FTCP : numpy ndarray
        FTCP representation as numpy ndarray.
    pad_width : int
        Number of values padded to the end of the second dimension.

    Returns
    -------
    FTCP : numpy ndarray
        Padded FTCP representation.

    '''
    
    FTCP = np.pad(FTCP, ((0, 0), (0, pad_width), (0, 0)), constant_values=0)
    return FTCP

def minmax(FTCP):
    '''
    This function performs data normalization for FTCP representation along the second dimension

    Parameters
    ----------
    FTCP : numpy ndarray
        FTCP representation as numpy ndarray.

    Returns
    -------
    FTCP_normed : numpy ndarray
        Normalized FTCP representation.
    scaler : sklearn MinMaxScaler object
        MinMaxScaler used for the normalization.

    '''
    
    dim0, dim1, dim2 = FTCP.shape
    scaler = MinMaxScaler()
    FTCP_ = np.transpose(FTCP, (1, 0, 2))
    FTCP_ = FTCP_.reshape(dim1, dim0*dim2)
    FTCP_ = scaler.fit_transform(FTCP_.T)
    FTCP_ = FTCP_.T
    FTCP_ = FTCP_.reshape(dim1, dim0, dim2)
    FTCP_normed = np.transpose(FTCP_, (1, 0, 2))
    
    return FTCP_normed, scaler

def inv_minmax(FTCP_normed, scaler):
    '''
    This function is the inverse of minmax, 
    which denormalize the FTCP representation along the second dimension

    Parameters
    ----------
    FTCP_normed : numpy ndarray
        Normalized FTCP representation.
    scaler : sklearn MinMaxScaler object
        MinMaxScaler used for the normalization.

    Returns
    -------
    FTCP : numpy ndarray
        Denormalized FTCP representation as numpy ndarray.

    '''
    dim0, dim1, dim2 = FTCP_normed.shape

    FTCP_ = np.transpose(FTCP_normed, (1, 0, 2))
    FTCP_ = FTCP_.reshape(dim1, dim0*dim2)
    FTCP_ = scaler.inverse_transform(FTCP_.T)
    FTCP_ = FTCP_.T
    FTCP_ = FTCP_.reshape(dim1, dim0, dim2)
    FTCP = np.transpose(FTCP_, (1, 0, 2))
    
    return FTCP
    
def get_secret(secret_name, region_name='us-west-2'):
    import boto3
    from botocore.exceptions import ClientError
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret " + secret_name + " was not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print("The request was invalid due to:", e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print("The request had invalid params:", e)
    else:
        # Secrets Manager decrypts the secret value using the associated KMS CMK
        # Depending on whether the secret was a string or binary, only one of these fields will be populated
        if 'SecretString' in get_secret_value_response:
            text_secret_data = get_secret_value_response['SecretString']
            return json.loads(text_secret_data)
        else:
            binary_secret_data = get_secret_value_response['SecretBinary']
            return binary_secret_data
            