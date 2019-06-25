
import math
import json
#bd墨卡托转BD-09
def Yr(lnglat,b):
    if b!='':
        c=b[0]+b[1]*abs(lnglat[0])
        d=abs(lnglat[1]/b[9])
        d=b[2]+b[3]*d+b[4]*d*d+b[5]*d*d*d+b[6]*d*d*d*d+b[7]*d*d*d*d*d+b[8]*d*d*d*d*d*d
        if 0>lnglat[0]:
            bd=-1*c
        else:
            bd=c
        lnglat[0]=bd
        if 0 > lnglat[0]:
            bd2 = -1 * d
        else:
            bd2 = d
        lnglat[1] = bd2
        return lnglat
    return
def Mecator2BD09(lng,lat):
    lnglat=[0,0]
    Au=[[1.410526172116255E-8, 8.98305509648872E-6, -1.9939833816331, 200.9824383106796, -187.2403703815547,
          91.6087516669843, -23.38765649603339, 2.57121317296198, -0.03801003308653, 1.73379812E7],
         [- 7.435856389565537E-9, 8.983055097726239E-6, -0.78625201886289, 96.32687599759846, -1.85204757529826,
          -59.36935905485877, 47.40033549296737, -16.50741931063887, 2.28786674699375, 1.026014486E7],
         [- 3.030883460898826E-8, 8.98305509983578E-6, 0.30071316287616, 59.74293618442277, 7.357984074871,
          -25.38371002664745, 13.45380521110908, -3.29883767235584, 0.32710905363475, 6856817.37],
         [- 1.981981304930552E-8, 8.983055099779535E-6, 0.03278182852591, 40.31678527705744, 0.65659298677277,
          -4.44255534477492, 0.85341911805263, 0.12923347998204, -0.04625736007561, 4482777.06],
         [3.09191371068437E-9, 8.983055096812155E-6, 6.995724062E-5, 23.10934304144901, -2.3663490511E-4,
          -0.6321817810242, -0.00663494467273, 0.03430082397953, -0.00466043876332, 2555164.4],
         [2.890871144776878E-9, 8.983055095805407E-6, -3.068298E-8, 7.47137025468032, -3.53937994E-6, -0.02145144861037,
          -1.234426596E-5, 1.0322952773E-4, -3.23890364E-6, 826088.5]]
    Sp=[1.289059486E7, 8362377.87, 5591021, 3481989.83, 1678043.12, 0 ]
    lnglat[0]=math.fabs(lng)
    lnglat[1] =abs(lat)
    for d in range(0,6):
        if lnglat[1]>=Sp[d]:
            c=Au[d]
            break
    lnglat=Yr(lnglat,c)
    return lnglat

def bd09_to_gcj02(lnglat):
    """
    百度坐标系(BD-09)转火星坐标系(GCJ-02)：百度——>谷歌、高德
    :param bd_lat:百度坐标纬度
    :param bd_lon:百度坐标经度
    :return:列表返回
    """
    x = lnglat[0] - 0.0065
    y = lnglat[1] - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gc_lng = z * math.cos(theta)
    gc_lat = z * math.sin(theta)
    return (gc_lng, gc_lat)

if __name__=='__main__':
    pi = 3.1415926535897932384626  # π
    x_pi = 3.14159265358979324 * 3000.0 / 180.0 
    
    with open("C:/Users/Lenovo/Desktop/shoucang.json", 'r') as f:
        load_dict = json.load(f)

    results = load_dict['sync']['newdata']
    shoucang = []
    for result in results:
        if result['action'] == 'del':
            continue
        try:
            extdata = result['detail']['data']['extdata']
            name = extdata['name']
            geoptx = int(extdata['geoptx'])
            geopty = int(extdata['geopty'])
            ptxy=bd09_to_gcj02(Mecator2BD09(geoptx, geopty))
            shoucang.append({'name':name, 'ptxy':ptxy})
        except KeyError:
            print("数据没找到，跳过")
    with open("C:/Users/Lenovo/Desktop/shuju.json", 'w') as f:
        f.write(str(shoucang))
    print(shoucang)
    print(len(shoucang))
