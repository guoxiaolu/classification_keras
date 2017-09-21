import keras.backend as K
from keras.applications import InceptionV3
from keras.layers import Dense
from keras.models import Model

def processing_function(x):
    if K.image_dim_ordering() == 'th':
        x = x.transpose((1, 2, 0))
    # Remove zero-center by mean pixel, RGB mode
    x[:, :, 0] -= 123.68
    x[:, :, 1] -= 116.779
    x[:, :, 2] -= 103.939
    return x

def InceptionV3_model(nb_classes):
    # load model
    basemodel = InceptionV3()
    input = basemodel.input
    x = basemodel.get_layer('avg_pool').output
    output = Dense(nb_classes, activation='softmax', name='prediction')(x)
    model = Model(input, output)

    return model

def write2html(txtname, htmlname):
    txt = open(txtname, 'r')
    myDic = {}
    for row in txt:
        split_result = row.strip().split('\t')
        if len(split_result) == 0:
            continue
        img_path = split_result[-1]
        img_path = img_path.replace(' ', '%20')
        result = split_result[:-1]

        myDic[img_path]=result

    print myDic

    fout=open(htmlname, 'w')
    html = '<html>'
    html += '<head>'
    html += '<meta http-equiv="Content-Type" content="text/html"; charset=utf-8 />'
    html += '</head>'
    html += '<body>'

    for img_path, result in myDic.iteritems():
        html += '<h6 align="center">%s\t%s\t%s\t%s</h6>' % (result[0],result[1],result[2],result[3])
        html += '<div align="center"><img src=%s width="600"  /></div>' % img_path
    html += '</body>'
    html += '</html>'
    fout.write(html)
    fout.close()