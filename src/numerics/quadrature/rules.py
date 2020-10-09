import numpy as np


'''
Dictionaries: QuadLinePoints, QuadLineWeights
-------------------
These dictionaries store the Gauss-Legendre quadrature points and weights for the reference line segment

USAGE:
    QuadLinePoints[Order] = quadrature points for Gauss-Legendre quadrature of Order Order
    QuadLineWeights[Order] = quadrature weights for Gauss-Legendre quadrature of Order Order
'''
QuadLinePoints = {}
QuadLineWeights = {}
for key in [0,1]:
	# Order 1
	QuadLinePoints[key] = np.array([0.0])
	QuadLineWeights[key] = np.array([2.0])
for key in [2,3]:
	# Order 3
	QuadLinePoints[key] = np.array([-0.5773502691896258, 0.5773502691896258])
	QuadLineWeights[key] = np.array([1.000000000000000, 1.000000000000000])
for key in [4,5]:
	# Order 5
	QuadLinePoints[key] = np.array([-0.774596669241483, 0.000000000000000, 0.774596669241483])
	QuadLineWeights[key] = np.array([0.5555555555555556, 0.8888888888888889, 0.5555555555555556])
for key in [6,7]:
	# Order 7
	QuadLinePoints[key] = np.array([-0.861136311594053, -0.339981043584856, 0.339981043584856, 0.861136311594053])
	QuadLineWeights[key] = np.array([0.3478548451374539, 0.6521451548625461, 0.6521451548625461, 0.3478548451374539])
for key in [8,9]:
	# Order 9
	QuadLinePoints[key] = np.array([-0.906179845938664, -0.5384693101056830, 0.000000000000000, 0.5384693101056830,
    0.9061798459386639])
	QuadLineWeights[key] = np.array([0.2369268850561891, 0.478628670499366468, 0.568888888888889, 0.478628670499366468,
    0.2369268850561891])
for key in [10,11]:
	# Order 11
	QuadLinePoints[key] = np.array([-0.9324695142031520, -0.6612093864662645, -0.2386191860831969, 0.2386191860831969,
    0.6612093864662645, 0.9324695142031520])
	QuadLineWeights[key] = np.array([0.17132449237917034, 0.36076157304813860, 0.46791393457269104, 0.46791393457269104,
    0.36076157304813860, 0.17132449237917034])
for key in [12,13]:
	# Order 13
	QuadLinePoints[key] = np.array([-0.94910791234275852, -0.74153118559939443, -0.40584515137739716, 0.000000000000000,
    0.40584515137739716, 0.74153118559939443, 0.94910791234275852])
	QuadLineWeights[key] = np.array([0.1294849661688697, 0.27970539148927666, 0.38183005050511894, 0.41795918367346938,
    0.38183005050511894, 0.27970539148927666, 0.1294849661688697])
for key in [14,15]:
	# Order 15
	QuadLinePoints[key] = np.array([-0.9602898564975362, -0.7966664774136267, -0.5255324099163289, -0.1834346424956498,
    0.1834346424956498, 0.5255324099163289, 0.7966664774136267, 0.9602898564975362])
	QuadLineWeights[key] = np.array([0.1012285362903763, 0.2223810344533744, 0.3137066458778872, 0.3626837833783619,
    0.3626837833783619, 0.3137066458778872, 0.2223810344533744, 0.1012285362903763])
for key in [16,17]:
	# Order 17
	QuadLinePoints[key] = np.array([-0.96816023950762608, -0.83603110732663579, -0.61337143270059039, -0.32425342340380892,
    0.000000000000000, 0.32425342340380892, 0.61337143270059039, 0.83603110732663579, 
    0.96816023950762608])
	QuadLineWeights[key] = np.array([0.0812743883615744, 0.1806481606948574, 0.2606106964029354, 0.3123470770400028,
    0.3302393550012597, 0.3123470770400028, 0.2606106964029354, 0.1806481606948574, 
    0.0812743883615744])
for key in [18,19]:
	# Order 19
	QuadLinePoints[key] = np.array([-0.9739065285171717, -0.8650633666889845, -0.6794095682990244, -0.4333953941292471,
    -0.1488743389816312, 0.1488743389816312, 0.4333953941292471, 0.6794095682990244,
    0.8650633666889845, 0.9739065285171717])
	QuadLineWeights[key] = np.array([0.0666713443086881, 0.1494513491505805, 0.2190863625159820, 0.2692667193099963,
    0.2955242247147528, 0.2955242247147528, 0.2692667193099963, 0.2190863625159820,
    0.1494513491505805, 0.0666713443086881])
for key in [20,21]:
	# Order 21
	QuadLinePoints[key] = np.array([-0.9782286581460569, -0.8870625997680952, -0.7301520055740493, -0.5190961292068118,
    -0.2695431559523449, 0.000000000000000, 0.2695431559523449, 0.5190961292068118,
    0.7301520055740493, 0.8870625997680952, 0.9782286581460569])
	QuadLineWeights[key] = np.array([0.0556685671161736, 0.1255803694649046, 0.1862902109277342, 0.2331937645919904,
    0.2628045445102466, 0.2729250867779006, 0.2628045445102466, 0.2331937645919904,
    0.1862902109277342, 0.1255803694649046, 0.0556685671161736])
for key in [22,23]:
	# Order 23
	QuadLinePoints[key] = np.array([-0.9815606342467192, -0.9041172563704748, -0.7699026741943046, -0.5873179542866174,
    -0.3678314989981801, -0.1252334085114689, 0.1252334085114689, 0.3678314989981801,
    0.5873179542866174, 0.7699026741943046, 0.9041172563704748, 0.9815606342467192])
	QuadLineWeights[key] = np.array([0.0471753363865118, 0.1069393259953184, 0.1600783285433462, 0.2031674267230659,
    0.23349253653835480, 0.24914704581340278, 0.24914704581340278, 0.23349253653835480,
    0.2031674267230659, 0.1600783285433462, 0.1069393259953184, 0.0471753363865118])
for key in [24,25]:
	# Order 21
	QuadLinePoints[key] = np.array([-0.9841830547185881, -0.9175983992229779, -0.8015780907333099, -0.6423493394403402,
    -0.4484927510364468, -0.2304583159551347, 0.000000000000000, 0.2304583159551347,
    0.4484927510364468, 0.6423493394403402, 0.8015780907333099, 0.9175983992229779,
    0.9841830547185881])
	QuadLineWeights[key] = np.array([0.0404840047653158, 0.0921214998377284, 0.1388735102197872, 0.1781459807619457,
    0.2078160475368885, 0.2262831802628972, 0.2325515532308739, 0.2262831802628972,
    0.2078160475368885,0.1781459807619457, 0.1388735102197872, 0.0921214998377284,
    0.0404840047653158])
for key in [26,27]:
	# Order 21
	QuadLinePoints[key] = np.array([-0.9862838086968123, -0.9284348836635735, -0.8272013150697649, -0.6872929048116854,
    -0.5152486363581540, -0.3191123689278897, -0.1080549487073436, 0.1080549487073436,
    0.3191123689278897, 0.5152486363581540, 0.6872929048116854, 0.8272013150697649,
    0.9284348836635735, 0.9862838086968123])
	QuadLineWeights[key] = np.array([0.0351194603317518, 0.0801580871597602, 0.1215185706879031, 0.1572031671581935,
    0.1855383974779378, 0.2051984637212956, 0.215263853463157, 0.215263853463157,
    0.2051984637212956, 0.1855383974779378, 0.1572031671581935, 0.1215185706879031,
    0.0801580871597602, 0.0351194603317518])
# reshape
for Order in QuadLinePoints.keys():
	QuadLinePoints[Order].shape = -1,1
	QuadLineWeights[Order].shape = -1,1


'''
Dictionaries: QuadLinePoints, QuadLineWeights
-------------------
These dictionaries store the Gauss-Legendre quadrature points and weights for the reference quadrilateral

USAGE:
    QuadQuadrilateralPoints[Order] = quadrature points for Gauss-Legendre quadrature of Order Order in each direction
    QuadQuadrilateralWeights[Order] = quadrature weights for Gauss-Legendre quadrature of Order Order in each direction
'''
QuadQuadrilateralPoints = {}
QuadQuadrilateralWeights = {}
# Obtain from line segment quadrature
for order in QuadLinePoints.keys():
    # Extract quadrature info for reference line segment
    xqline = QuadLinePoints[order]
    wqline = QuadLineWeights[order]
    nqline = len(xqline)
    nquad = nqline**2
    quad_wts = np.zeros([nquad,1])
    quad_pts = np.zeros([nquad,2])
    # iq = 0
    # for j in range(nqline):
    # 	xqj = xqline[j]
    # 	wqj = wqline[j]
    # 	for i in range(nqline):
    # 		xqi = xqline[i]
    # 		wqi = wqline[i]

    # 		quad_wts[iq] = wqi*wqj
    # 		quad_pts[iq,0] = xqi
    # 		quad_pts[iq,1] = xqj
    # 		iq += 1

    # if iq != nquad:
    # 	raise ValueError
    quad_wts[:] = np.reshape(np.outer(wqline, wqline), (-1,), 'F').reshape(-1,1)
    quad_pts[:,0] = np.tile(xqline, (nqline,1)).reshape(-1)
    quad_pts[:,1] = np.repeat(xqline, nqline, axis=0).reshape(-1)

    # Store in dictionaries
    QuadQuadrilateralPoints[order] = quad_pts
    QuadQuadrilateralWeights[order] = quad_wts


'''
Dictionaries: QuadTrianglePoints, QuadTriangleWeights
-------------------
These dictionaries store the Gauss-Legendre quadrature points and weights for the reference triangle

USAGE:
    QuadTrianglePoints[Order] = quadrature points for Gauss-Legendre quadrature of Order Order in each direction
    QuadTriangleWeights[Order] = quadrature weights for Gauss-Legendre quadrature of Order Order in each direction
'''
QuadTrianglePoints = {}
QuadTriangleWeights = {}
for key in [0,1]:
	# Order 1
	QuadTrianglePoints[key] = np.array([0.333333333333333, 0.333333333333333])
	QuadTriangleWeights[key] = np.array([0.500000000000000])
for key in [2]:
	# Order 1
	QuadTrianglePoints[key] = np.array([0.666666666666667, 0.166666666666667, 0.166666666666667, 0.166666666666667,
    0.166666666666667, 0.666666666666667])
	QuadTriangleWeights[key] = np.array([0.166666666666666, 0.166666666666666, 0.166666666666666])
for key in [3]:
	# Order 1
	QuadTrianglePoints[key] = np.array([0.333333333333333, 0.333333333333333, 0.600000000000000, 0.200000000000000,
    0.200000000000000, 0.200000000000000, 0.200000000000000, 0.600000000000000])
	QuadTriangleWeights[key] = np.array([-0.281250000000000, 0.260416666666667, 0.260416666666667, 0.260416666666667])
for key in [4]:
	# Order 1
	QuadTrianglePoints[key] = np.array([0.108103018168070, 0.445948490915965, 0.445948490915965, 0.445948490915965,
    0.445948490915965, 0.108103018168070, 0.816847572980459, 0.091576213509771,
    0.091576213509771, 0.091576213509771, 0.091576213509771, 0.816847572980459])
	QuadTriangleWeights[key] = np.array([0.111690794839005, 0.111690794839005, 0.111690794839005, 0.054975871827661,
    0.054975871827661, 0.054975871827661])
for key in [5]:
	# Order 1
	QuadTrianglePoints[key] = np.array([0.333333333333333, 0.333333333333333, 0.059715871789770, 0.470142064105115,
    0.470142064105115, 0.470142064105115, 0.470142064105115, 0.059715871789770,
    0.797426985353087, 0.101286507323456, 0.101286507323456, 0.101286507323456,
    0.101286507323456, 0.797426985353087])
	QuadTriangleWeights[key] = np.array([0.112500000000000, 0.066197076394253, 0.066197076394253, 0.066197076394253,
    0.062969590272414, 0.062969590272414, 0.062969590272414])
for key in [6]:
	# Order 1
	QuadTrianglePoints[key] = np.array([0.501426509658179, 0.249286745170910, 0.249286745170910, 0.249286745170910,
    0.249286745170910, 0.501426509658179, 0.873821971016996, 0.063089014491502,
    0.063089014491502, 0.063089014491502, 0.063089014491502, 0.873821971016996,
    0.053145049844817, 0.310352451033784, 0.310352451033784, 0.636502499121399,
    0.636502499121399, 0.053145049844817, 0.310352451033784, 0.053145049844817,
    0.636502499121399, 0.310352451033784, 0.053145049844817, 0.636502499121399])
	QuadTriangleWeights[key] = np.array([0.058393137863189, 0.058393137863189, 0.058393137863189, 0.025422453185103,
    0.025422453185103, 0.025422453185103, 0.041425537809187, 0.041425537809187,
    0.041425537809187, 0.041425537809187, 0.041425537809187, 0.041425537809187])
for key in [7]:
	# Order 1
	QuadTrianglePoints[key] = np.array([0.333333333333333, 0.333333333333333, 0.479308067841920, 0.260345966079040,
    0.260345966079040, 0.260345966079040, 0.260345966079040, 0.479308067841920,
    0.869739794195568, 0.065130102902216, 0.065130102902216, 0.065130102902216,
    0.065130102902216, 0.869739794195568, 0.048690315425316, 0.312865496004874,
    0.312865496004874, 0.638444188569810, 0.638444188569810, 0.048690315425316,
    0.312865496004874, 0.048690315425316, 0.638444188569810, 0.312865496004874,
    0.048690315425316, 0.638444188569810])
	QuadTriangleWeights[key] = np.array([-0.074785022233841, 0.087807628716604, 0.087807628716604, 0.087807628716604,
    0.026673617804419, 0.026673617804419, 0.026673617804419, 0.038556880445128,
    0.038556880445128, 0.038556880445128, 0.038556880445128, 0.038556880445128,
    0.038556880445128])
for key in [8]:
	# Order 1
	QuadTrianglePoints[key] = np.array([    0.333333333333333, 0.333333333333333, 0.081414823414554, 0.459292588292723,
    0.459292588292723, 0.459292588292723, 0.459292588292723, 0.081414823414554,
    0.658861384496480, 0.170569307751760, 0.170569307751760, 0.170569307751760,
    0.170569307751760, 0.658861384496480, 0.898905543365938, 0.050547228317031,
    0.050547228317031, 0.050547228317031, 0.050547228317031, 0.898905543365938,
    0.008394777409958, 0.263112829634638, 0.263112829634638, 0.728492392955404,
    0.728492392955404, 0.008394777409958, 0.263112829634638, 0.008394777409958,
    0.728492392955404, 0.263112829634638, 0.008394777409958, 0.728492392955404])
	QuadTriangleWeights[key] = np.array([0.072157803838894, 0.047545817133642, 0.047545817133642, 0.047545817133642,
    0.051608685267359, 0.051608685267359, 0.051608685267359, 0.016229248811599,
    0.016229248811599, 0.016229248811599, 0.013615157087217, 0.013615157087217,
    0.013615157087217, 0.013615157087217, 0.013615157087217, 0.013615157087217])
for key in [9]:
	# Order 1
	QuadTrianglePoints[key] = np.array([0.333333333333333, 0.333333333333333, 0.020634961602525, 0.489682519198738,
    0.489682519198738, 0.489682519198738, 0.489682519198738, 0.020634961602525,
    0.125820817014127, 0.437089591492937, 0.437089591492937, 0.437089591492937,
    0.437089591492937, 0.125820817014127, 0.623592928761935, 0.188203535619033,
    0.188203535619033, 0.188203535619033, 0.188203535619033, 0.623592928761935,
    0.910540973211095, 0.044729513394453, 0.044729513394453, 0.044729513394453,
    0.044729513394453, 0.910540973211095, 0.036838412054736, 0.221962989160766,
    0.221962989160766, 0.741198598784498, 0.741198598784498, 0.036838412054736,
    0.221962989160766, 0.036838412054736, 0.741198598784498, 0.221962989160766,
    0.036838412054736, 0.741198598784498])
	QuadTriangleWeights[key] = np.array([0.048567898141400, 0.015667350113570, 0.015667350113570, 0.015667350113570,
    0.038913770502387, 0.038913770502387, 0.038913770502387, 0.039823869463605,
    0.039823869463605, 0.039823869463605, 0.012788837829349, 0.012788837829349,
    0.012788837829349, 0.021641769688645, 0.021641769688645, 0.021641769688645,
    0.021641769688645, 0.021641769688645, 0.021641769688645])
for key in [10]:
	# Order 1
	QuadTrianglePoints[key] = np.array([0.333333333333333, 0.333333333333333, 0.028844733232685, 0.485577633383657,
    0.485577633383657, 0.485577633383657, 0.485577633383657, 0.028844733232685,
    0.781036849029926, 0.109481575485037, 0.109481575485037, 0.109481575485037,
    0.109481575485037, 0.781036849029926, 0.141707219414880, 0.307939838764121,
    0.307939838764121, 0.550352941820999, 0.550352941820999, 0.141707219414880,
    0.307939838764121, 0.141707219414880, 0.550352941820999, 0.307939838764121,
    0.141707219414880, 0.550352941820999, 0.025003534762686, 0.246672560639903,
    0.246672560639903, 0.728323904597411, 0.728323904597411, 0.025003534762686,
    0.246672560639903, 0.025003534762686, 0.728323904597411, 0.246672560639903,
    0.025003534762686, 0.728323904597411, 0.009540815400299, 0.066803251012200,
    0.066803251012200, 0.923655933587500, 0.923655933587500, 0.009540815400299,
    0.066803251012200, 0.009540815400299, 0.923655933587500, 0.066803251012200,
    0.009540815400299, 0.923655933587500])
	QuadTriangleWeights[key] = np.array([0.045408995191377, 0.018362978878233, 0.018362978878233, 0.018362978878233,
    0.022660529717764, 0.022660529717764, 0.022660529717764, 0.036378958422710,
    0.036378958422710, 0.036378958422710, 0.036378958422710, 0.036378958422710,
    0.036378958422710, 0.014163621265528, 0.014163621265528, 0.014163621265528,
    0.014163621265528, 0.014163621265528, 0.014163621265528, 0.004710833481867,
    0.004710833481867, 0.004710833481867, 0.004710833481867, 0.004710833481867,
    0.004710833481867])
for key in [11,12]:
	# Order 1
	QuadTrianglePoints[key] = np.array([0.023565220452390, 0.488217389773805, 0.488217389773805, 0.488217389773805,
    0.488217389773805, 0.023565220452390, 0.120551215411079, 0.439724392294460,
    0.439724392294460, 0.439724392294460, 0.439724392294460, 0.120551215411079,
    0.457579229975768, 0.271210385012116, 0.271210385012116, 0.271210385012116,
    0.271210385012116, 0.457579229975768, 0.744847708916828, 0.127576145541586,
    0.127576145541586, 0.127576145541586, 0.127576145541586, 0.744847708916828,
    0.957365299093579, 0.021317350453210, 0.021317350453210, 0.021317350453210,
    0.021317350453210, 0.957365299093579, 0.115343494534698, 0.275713269685514,
    0.275713269685514, 0.608943235779788, 0.608943235779788, 0.115343494534698,
    0.275713269685514, 0.115343494534698, 0.608943235779788, 0.275713269685514,
    0.115343494534698, 0.608943235779788, 0.022838332222257, 0.281325580989940,
    0.281325580989940, 0.695836086787803, 0.695836086787803, 0.022838332222257,
    0.281325580989940, 0.022838332222257, 0.695836086787803, 0.281325580989940,
    0.022838332222257, 0.695836086787803, 0.025734050548330, 0.116251915907597,
    0.116251915907597, 0.858014033544073, 0.858014033544073, 0.025734050548330,
    0.116251915907597, 0.025734050548330, 0.858014033544073, 0.116251915907597,
    0.025734050548330, 0.858014033544073])
	QuadTriangleWeights[key] = np.array([0.012865533220227, 0.012865533220227, 0.012865533220227, 0.021846272269019,
    0.021846272269019, 0.021846272269019, 0.031429112108943, 0.031429112108943,
    0.031429112108943, 0.017398056465355, 0.017398056465355, 0.017398056465355,
    0.003083130525780, 0.003083130525780, 0.003083130525780, 0.020185778883191,
    0.020185778883191, 0.020185778883191, 0.020185778883191, 0.020185778883191,
    0.020185778883191, 0.011178386601152, 0.011178386601152, 0.011178386601152,
    0.011178386601152, 0.011178386601152, 0.011178386601152, 0.008658115554329,
    0.008658115554329, 0.008658115554329, 0.008658115554329, 0.008658115554329,
    0.008658115554329])
for key in [13]:
	# Order 1
	QuadTrianglePoints[key] = np.array([0.333333333333333, 0.333333333333333, 0.009903630120591, 0.495048184939705,
    0.495048184939705, 0.495048184939705, 0.495048184939705, 0.009903630120591,
    0.062566729780852, 0.468716635109574, 0.468716635109574, 0.468716635109574,
    0.468716635109574, 0.062566729780852, 0.170957326397447, 0.414521336801277,
    0.414521336801277, 0.414521336801277, 0.414521336801277, 0.170957326397447,
    0.541200855914337, 0.229399572042831, 0.229399572042831, 0.229399572042831,
    0.229399572042831, 0.541200855914337, 0.771151009607340, 0.114424495196330,
    0.114424495196330, 0.114424495196330, 0.114424495196330, 0.771151009607340,
    0.950377217273082, 0.024811391363459, 0.024811391363459, 0.024811391363459,
    0.024811391363459, 0.950377217273082, 0.094853828379579, 0.268794997058761,
    0.268794997058761, 0.636351174561660, 0.636351174561660, 0.094853828379579,
    0.268794997058761, 0.094853828379579, 0.636351174561660, 0.268794997058761,
    0.094853828379579, 0.636351174561660, 0.018100773278807, 0.291730066734288,
    0.291730066734288, 0.690169159986905, 0.690169159986905, 0.018100773278807,
    0.291730066734288, 0.018100773278807, 0.690169159986905, 0.291730066734288,
    0.018100773278807, 0.690169159986905, 0.022233076674090, 0.126357385491669,
    0.126357385491669, 0.851409537834241, 0.851409537834241, 0.022233076674090,
    0.126357385491669, 0.022233076674090, 0.851409537834241, 0.126357385491669,
    0.022233076674090, 0.851409537834241])
	QuadTriangleWeights[key] = np.array([0.026260461700401, 0.005640072604665, 0.005640072604665, 0.005640072604665,
    0.015711759181227, 0.015711759181227, 0.015711759181227, 0.023536251252097,
    0.023536251252097, 0.023536251252097, 0.023681793268178, 0.023681793268178,
    0.023681793268178, 0.015583764522897, 0.015583764522897, 0.015583764522897,
    0.003987885732537, 0.003987885732537, 0.003987885732537, 0.018424201364366,
    0.018424201364366, 0.018424201364366, 0.018424201364366, 0.018424201364366,
    0.018424201364366, 0.008700731651911, 0.008700731651911, 0.008700731651911,
    0.008700731651911, 0.008700731651911, 0.008700731651911, 0.007760893419522,
    0.007760893419522, 0.007760893419522, 0.007760893419522, 0.007760893419522,
    0.007760893419522])
for key in [14]:
	# Order 1
	QuadTrianglePoints[key] = np.array([0.022072179275643, 0.488963910362179, 0.488963910362179, 0.488963910362179,
    0.488963910362179, 0.022072179275643, 0.164710561319092, 0.417644719340454,
    0.417644719340454, 0.417644719340454, 0.417644719340454, 0.164710561319092,
    0.453044943382323, 0.273477528308839, 0.273477528308839, 0.273477528308839,
    0.273477528308839, 0.453044943382323, 0.645588935174913, 0.177205532412543,
    0.177205532412543, 0.177205532412543, 0.177205532412543, 0.645588935174913,
    0.876400233818255, 0.061799883090873, 0.061799883090873, 0.061799883090873,
    0.061799883090873, 0.876400233818255, 0.961218077502598, 0.019390961248701,
    0.019390961248701, 0.019390961248701, 0.019390961248701, 0.961218077502598,
    0.057124757403648, 0.172266687821356, 0.172266687821356, 0.770608554774996,
    0.770608554774996, 0.057124757403648, 0.172266687821356, 0.057124757403648,
    0.770608554774996, 0.172266687821356, 0.057124757403648, 0.770608554774996,
    0.092916249356972, 0.336861459796345, 0.336861459796345, 0.570222290846683,
    0.570222290846683, 0.092916249356972, 0.336861459796345, 0.092916249356972,
    0.570222290846683, 0.336861459796345, 0.092916249356972, 0.570222290846683,
    0.014646950055654, 0.298372882136258, 0.298372882136258, 0.686980167808088,
    0.686980167808088, 0.014646950055654, 0.298372882136258, 0.014646950055654,
    0.686980167808088, 0.298372882136258, 0.014646950055654, 0.686980167808088,
    0.001268330932872, 0.118974497696957, 0.118974497696957, 0.879757171370171,
    0.879757171370171, 0.001268330932872, 0.118974497696957, 0.001268330932872,
    0.879757171370171, 0.118974497696957, 0.001268330932872, 0.879757171370171])
	QuadTriangleWeights[key] = np.array([0.010941790684715, 0.010941790684715, 0.010941790684715, 0.016394176772063,
    0.016394176772063, 0.016394176772063, 0.025887052253646, 0.025887052253646,
    0.025887052253646, 0.021081294368497, 0.021081294368497, 0.021081294368497,
    0.007216849834889, 0.007216849834889, 0.007216849834889, 0.002461701801200,
    0.002461701801200, 0.002461701801200, 0.012332876606282, 0.012332876606282,
    0.012332876606282, 0.012332876606282, 0.012332876606282, 0.012332876606282,
    0.019285755393531, 0.019285755393531, 0.019285755393531, 0.019285755393531,
    0.019285755393531, 0.019285755393531, 0.007218154056767, 0.007218154056767,
    0.007218154056767, 0.007218154056767, 0.007218154056767, 0.007218154056767,
    0.002505114419250, 0.002505114419250, 0.002505114419250, 0.002505114419250,
    0.002505114419250, 0.002505114419250])
for key in [15,16,17]:
	# Order 1
	QuadTrianglePoints[key] = np.array([0.333333333333333, 0.333333333333333, 0.005658918886452, 0.497170540556774,
    0.497170540556774, 0.497170540556774, 0.497170540556774, 0.005658918886452,
    0.035647354750751, 0.482176322624625, 0.482176322624625, 0.482176322624625,
    0.482176322624625, 0.035647354750751, 0.099520061958437, 0.450239969020782,
    0.450239969020782, 0.450239969020782, 0.450239969020782, 0.099520061958437,
    0.199467521245206, 0.400266239377397, 0.400266239377397, 0.400266239377397,
    0.400266239377397, 0.199467521245206, 0.495717464058095, 0.252141267970953,
    0.252141267970953, 0.252141267970953, 0.252141267970953, 0.495717464058095,
    0.675905990683077, 0.162047004658461, 0.162047004658461, 0.162047004658461,
    0.162047004658461, 0.675905990683077, 0.848248235478508, 0.075875882260746,
    0.075875882260746, 0.075875882260746, 0.075875882260746, 0.848248235478508,
    0.968690546064356, 0.015654726967822, 0.015654726967822, 0.015654726967822,
    0.015654726967822, 0.968690546064356, 0.010186928826919, 0.334319867363658,
    0.334319867363658, 0.655493203809423, 0.655493203809423, 0.010186928826919,
    0.334319867363658, 0.010186928826919, 0.655493203809423, 0.334319867363658,
    0.010186928826919, 0.655493203809423, 0.135440871671036, 0.292221537796944,
    0.292221537796944, 0.572337590532020, 0.572337590532020, 0.135440871671036,
    0.292221537796944, 0.135440871671036, 0.572337590532020, 0.292221537796944,
    0.135440871671036, 0.572337590532020, 0.054423924290583, 0.319574885423190,
    0.319574885423190, 0.626001190286228, 0.626001190286228, 0.054423924290583,
    0.319574885423190, 0.054423924290583, 0.626001190286228, 0.319574885423190,
    0.054423924290583, 0.626001190286228, 0.012868560833637, 0.190704224192292,
    0.190704224192292, 0.796427214974071, 0.796427214974071, 0.012868560833637,
    0.190704224192292, 0.012868560833637, 0.796427214974071, 0.190704224192292,
    0.012868560833637, 0.796427214974071, 0.067165782413524, 0.180483211648746,
    0.180483211648746, 0.752351005937729, 0.752351005937729, 0.067165782413524,
    0.180483211648746, 0.067165782413524, 0.752351005937729, 0.180483211648746,
    0.067165782413524, 0.752351005937729, 0.014663182224828, 0.080711313679564,
    0.080711313679564, 0.904625504095608, 0.904625504095608, 0.014663182224828,
    0.080711313679564, 0.014663182224828, 0.904625504095608, 0.080711313679564,
    0.014663182224828, 0.904625504095608])
	QuadTriangleWeights[key] = np.array([0.016718599645402, 0.002546707720254, 0.002546707720254, 0.002546707720254,
    0.007335432263819, 0.007335432263819, 0.007335432263819, 0.012175439176836,
    0.012175439176836, 0.012175439176836, 0.015553775434484, 0.015553775434484,
    0.015553775434484, 0.015628555609310, 0.015628555609310, 0.015628555609310,
    0.012407827169833, 0.012407827169833, 0.012407827169833, 0.007028036535279,
    0.007028036535279, 0.007028036535279, 0.001597338086889, 0.001597338086889,
    0.001597338086889, 0.004059827659497, 0.004059827659497, 0.004059827659497,
    0.004059827659497, 0.004059827659497, 0.004059827659497, 0.013402871141582,
    0.013402871141582, 0.013402871141582, 0.013402871141582, 0.013402871141582,
    0.013402871141582, 0.009229996605411, 0.009229996605411, 0.009229996605411,
    0.009229996605411, 0.009229996605411, 0.009229996605411, 0.004238434267164,
    0.004238434267164, 0.004238434267164, 0.004238434267164, 0.004238434267164,
    0.004238434267164, 0.009146398385012, 0.009146398385012, 0.009146398385012,
    0.009146398385012, 0.009146398385012, 0.009146398385012, 0.003332816002083,
    0.003332816002083, 0.003332816002083, 0.003332816002083, 0.003332816002083,
    0.003332816002083])
for key in [18,19]:
	# Order 1
	QuadTrianglePoints[key] = np.array([0.333333333333333, 0.333333333333333, 0.020780025853987, 0.489609987073006,
    0.489609987073006, 0.489609987073006, 0.489609987073006, 0.020780025853987,
    0.090926214604215, 0.454536892697893, 0.454536892697893, 0.454536892697893,
    0.454536892697893, 0.090926214604215, 0.197166638701138, 0.401416680649431,
    0.401416680649431, 0.401416680649431, 0.401416680649431, 0.197166638701138,
    0.488896691193805, 0.255551654403098, 0.255551654403098, 0.255551654403098,
    0.255551654403098, 0.488896691193805, 0.645844115695741, 0.177077942152130,
    0.177077942152130, 0.177077942152130, 0.177077942152130, 0.645844115695741,
    0.779877893544096, 0.110061053227952, 0.110061053227952, 0.110061053227952,
    0.110061053227952, 0.779877893544096, 0.888942751496321, 0.055528624251840,
    0.055528624251840, 0.055528624251840, 0.055528624251840, 0.888942751496321,
    0.974756272445543, 0.012621863777229, 0.012621863777229, 0.012621863777229,
    0.012621863777229, 0.974756272445543, 0.003611417848412, 0.395754787356943,
    0.395754787356943, 0.600633794794645, 0.600633794794645, 0.003611417848412,
    0.395754787356943, 0.003611417848412, 0.600633794794645, 0.395754787356943,
    0.003611417848412, 0.600633794794645, 0.134466754530780, 0.307929983880436,
    0.307929983880436, 0.557603261588784, 0.557603261588784, 0.134466754530780,
    0.307929983880436, 0.134466754530780, 0.557603261588784, 0.307929983880436,
    0.134466754530780, 0.557603261588784, 0.014446025776115, 0.264566948406520,
    0.264566948406520, 0.720987025817365, 0.720987025817365, 0.014446025776115,
    0.264566948406520, 0.014446025776115, 0.720987025817365, 0.264566948406520,
    0.014446025776115, 0.720987025817365, 0.046933578838178, 0.358539352205951,
    0.358539352205951, 0.594527068955871, 0.594527068955871, 0.046933578838178,
    0.358539352205951, 0.046933578838178, 0.594527068955871, 0.358539352205951,
    0.046933578838178, 0.594527068955871, 0.002861120350567, 0.157807405968595,
    0.157807405968595, 0.839331473680839, 0.839331473680839, 0.002861120350567,
    0.157807405968595, 0.002861120350567, 0.839331473680839, 0.157807405968595,
    0.002861120350567, 0.839331473680839, 0.223861424097916, 0.075050596975911,
    0.075050596975911, 0.701087978926173, 0.701087978926173, 0.223861424097916,
    0.075050596975911, 0.223861424097916, 0.701087978926173, 0.075050596975911,
    0.223861424097916, 0.701087978926173, 0.034647074816760, 0.142421601113383,
    0.142421601113383, 0.822931324069857, 0.822931324069857, 0.034647074816760,
    0.142421601113383, 0.034647074816760, 0.822931324069857, 0.142421601113383,
    0.034647074816760, 0.822931324069857, 0.010161119296278, 0.065494628082938,
    0.065494628082938, 0.924344252620784, 0.924344252620784, 0.010161119296278,
    0.065494628082938, 0.010161119296278, 0.924344252620784, 0.065494628082938,
    0.010161119296278, 0.924344252620784])
	QuadTriangleWeights[key] = np.array([0.016453165694459, 0.005165365945636, 0.005165365945636, 0.005165365945636,
    0.011193623631508, 0.011193623631508, 0.011193623631508, 0.015133062934734,
    0.015133062934734, 0.015133062934734, 0.015245483901099, 0.015245483901099,
    0.015245483901099, 0.012079606370821, 0.012079606370821, 0.012079606370821,
    0.008025401793400, 0.008025401793400, 0.008025401793400, 0.004042290130892,
    0.004042290130892, 0.004042290130892, 0.001039681013742, 0.001039681013742,
    0.001039681013742, 0.001942438452491, 0.001942438452491, 0.001942438452491,
    0.001942438452491, 0.001942438452491, 0.001942438452491, 0.012787080306011,
    0.012787080306011, 0.012787080306011, 0.012787080306011, 0.012787080306011,
    0.012787080306011, 0.004440451786669, 0.004440451786669, 0.004440451786669,
    0.004440451786669, 0.004440451786669, 0.004440451786669, 0.008062273380866,
    0.008062273380866, 0.008062273380866, 0.008062273380866, 0.008062273380866,
    0.008062273380866, 0.001245970908745, 0.001245970908745, 0.001245970908745,
    0.001245970908745, 0.001245970908745, 0.001245970908745, 0.009121420059476,
    0.009121420059476, 0.009121420059476, 0.009121420059476, 0.009121420059476,
    0.009121420059476, 0.005129281868099, 0.005129281868099, 0.005129281868099,
    0.005129281868099, 0.005129281868099, 0.005129281868099, 0.001899964427651,
    0.001899964427651, 0.001899964427651, 0.001899964427651, 0.001899964427651,
    0.001899964427651])
# reshape
for order in QuadTrianglePoints.keys():
    QuadTrianglePoints[order].shape = -1,2
    QuadTriangleWeights[order].shape = -1,1

    # pts = QuadQuadrilateralPoints[order]
    # wts = QuadQuadrilateralWeights[order]

    # # Transform
    # wts[:,0] *= 0.125*(1. - pts[:,0])
    # pts[:,1] = 0.25*(1. - pts[:,0])*(1. + pts[:,1])
    # pts[:,0] = 0.5*(1. + pts[:,0])

    # QuadTrianglePoints[order] = pts
    # QuadTriangleWeights[order] = wts




