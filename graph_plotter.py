import matplotlib.pyplot as plt

# 자주 사용되는 단위 정의
MILI = 10 ** (-3)
MICRO = 10 ** (-6)

# 파형 신호를 저장해둘 배열 생성
original_waves = list()
rlc_waves = list()

# Data 파일 형식
# 측정한 주파수를 입력해주세요 : 
# 주파수값
# 사용한 저항값을 Ohm 단위로 입력해주세요 : 
# 저항값
# 사용한 L값을 mH 단위로 입력해주세요 : 
# L값
# 사용한 C값을 uF 단위로 입력해주세요 : 
# C값
# 사용한 R2값을 Ohm 단위로 입력해주세요(없으면 0입력) : 
# R2값
# R : ##Ohm, L : ##mH, C : ##uF, R2: ##Ohm
# 데이터들
# 단일 채널의 샘플당 측정 시간:
# 샘플당 측정 시간

with open("data.txt", "r", encoding='UTF-8') as file:
    lines = file.readlines()
    sample_count = len(lines) - 12
    freq = float(lines[1])
    R = float(lines[3])
    L = float(lines[5])
    C = float(lines[7])
    R2 = float(lines[9])
    for line in lines[10:-2]:
        delimited = line.split(';')
        targets = [original_waves, rlc_waves]
        for i in range(len(targets)):
            targets[i].append(int(delimited[i]))

    T = 1/freq
    sample_delay = int(lines[-1])   #microsecond 단위로 표기 (224us -> 224)
    sample_per_wave = T/ (sample_delay * MICRO)

print(f"freq : {freq}Hz, sample_delay : {sample_delay}us, sample_per_wave : {sample_per_wave}")
print(f"R : {R}Ohm, L : {L}mH, C : {C}uF, R2 : {R2}Ohm")

# 신호 해상도를 2배로 늘리도록 선형 보간으로 채움
time = [sample_delay/2 * i for i in range(sample_count * 2)]    # [0, 1/2 sample_delay, 1 sample_delay, ...]
interpolated_original_waves = [0 for i in range(sample_count * 2)]
interpolated_rlc_waves = [0 for i in range(sample_count * 2)]
for i in range(sample_count):
    interpolated_original_waves[2*i] = original_waves[i]
    interpolated_rlc_waves[2*i] = rlc_waves[i]
    if i != sample_count -1 :
        interpolated_original_waves[2 * i + 1] = (original_waves[i] + original_waves[i+1]) / 2 # 맨 뒤에건 interpolate 할 수 없으므로 그냥 마지막 값을 한번 더 씀
        interpolated_rlc_waves[2 * i + 1] = (rlc_waves[i] + rlc_waves[i+1]) / 2
    else :
        interpolated_original_waves[2 * i + 1] = original_waves[i]    # 맨 뒤에건 interpolate 할 수 없으므로 그냥 마지막 값을 한번 더 씀
        interpolated_rlc_waves[2 * i + 1] = rlc_waves[i]

# 측정 지연 반영
# 맨 뒤 요소를 제거하고 맨 앞에 요소를 새로 추가 -> 1/2 sample_delay만큼 뒤로 늦추어 측정 지연을 반영
interpolated_and_shifted_rlc_waves = interpolated_rlc_waves.copy()
interpolated_and_shifted_rlc_waves.pop(len(interpolated_and_shifted_rlc_waves)-1)
interpolated_and_shifted_rlc_waves.insert(0, interpolated_and_shifted_rlc_waves[0])

# 원본 전압 신호와 시간 지연을 반영한 RLC 전압 신호를 한 창에 모두 그림 
plt.plot(time, interpolated_original_waves, label='Ori', color='gold', marker='o')
plt.plot(time, interpolated_and_shifted_rlc_waves, label='RLC', color='green', marker='o')
plt.xlabel("time(us)")
plt.ylabel("rel volt(0~5v -> 0~1023)")
plt.ylim((0, 160))


# # 첫번째 극댓값에 수직선을 그어 위상차를 보기 좋게 만듬
# ori_local_max_idx = -1
# rlc_local_max_idx = -1
# for i in range(1, sample_count):
#     if interpolated_original_waves[i-1] < interpolated_original_waves[i] and interpolated_original_waves[i] > interpolated_original_waves[i+1]:
#         if ori_local_max_idx == -1 :
#             ori_local_max_idx = i
#     if  interpolated_and_shifted_rlc_waves[i-1] < interpolated_and_shifted_rlc_waves[i] and interpolated_and_shifted_rlc_waves[i] > interpolated_and_shifted_rlc_waves[i+1]:
#         if rlc_local_max_idx == -1:
#             rlc_local_max_idx = i

# ori_local_max_time = sample_delay * 0.5 * ori_local_max_idx
# rlc_local_max_time = sample_delay * 0.5 * rlc_local_max_idx

# print(f"ori_local_max_idx: {ori_local_max_idx}({ori_local_max_time}us), rlc_local_max_idx : {rlc_local_max_idx}({rlc_local_max_time}us))")
# plt.axvline(ori_local_max_time, 0, 1, color='purple', linestyle='--')
# plt.axvline(rlc_local_max_time, 0, 1, color='purple', linestyle='--')

# # 위상차 계산
# t_diff = rlc_local_max_time - ori_local_max_time
# # phase_difference = 360 * t_diff * MICRO * 2 / T

# plt.title(f"Uno Analog Input Signal (freq:{freq}Hz, Sample Delay:{sample_delay}us(res : {1/(sample_delay*MICRO):.3f}Hz))\n{R}Ohm, {L}mH, {C}uF, (R2 : {R2}Ohm) (Shift compensated)\n Phase Difference = {phase_difference}°")
plt.title(f"Uno Analog Input Signal (freq:{freq}Hz, Sample Delay:{sample_delay}us(res : {1/(sample_delay*MICRO):.3f}Hz))\n{R}Ohm, {L}mH, {C}uF, (R2 : {R2}Ohm) (Shift compensated)")
plt.show()