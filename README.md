# mptcp
dynamic_ixia.log 以下均是一行内容的解释，分为三个阶段，非切换期，切换准备期，切换执行期

线路 模式 一次周期循环开始时间 一次周期循环结束时间 
delayMind delayMax pdvMode interval	burstlen dist bitrate 持续时间a 
delayMind delayMax pdvMode interval burstlen dist bitrate y参数 持续时间b1 
delayMind delayMax pdvMode interval burstlen dist bitrate y参数 持续时间b2

----------------------------------------------------------------------------------------
static_ixia.log  数据中连续两行是一次设置中的两个线路 

线路 时间 delayMin,delayMax,pdvMode,interval,burstlen,dist,stddev,bitRate


----------------------------------------------------------------------------------------

static_run.sh 是静态配置测试脚本 调用static_ixia.py
使用方法： ./static_run.sh Test 1 1 1
第一个参数Test 是路径名称 
第二个参数 RTT模式
第三个参数 丢包模式
第四个参数 带宽模式
--------------------------------------------------------------
dynamic_run.sh 是动态配置测试脚本 调用dynamic_ixia.py
使用方法： ./dynamic_run.sh Test 1
第一个参数：路径名
第二个参数：模式
