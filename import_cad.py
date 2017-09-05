output_autocad = '''
                  LWPOLYLINE  Layer: "graveren"
                            Space: Model space

          at point  X=-48628.2250  Y=-17699.1477  Z=   0.0000
          at point  X=-49213.7585  Y=-17755.5587  Z=   0.0000
          at point  X=-49541.7998  Y=-17787.1627  Z=   0.0000
          at point  X=-49848.0964  Y=-15313.1147  Z=   0.0000
          at point  X=-51345.0596  Y=-15495.9004  Z=   0.0000
          at point  X=-51791.0742  Y=-11843.1662  Z=   0.0000
          at point  X=-51694.7516  Y=-11831.4048  Z=   0.0000
          at point  X=-51742.9011  Y=-11474.8481  Z=   0.0000
          at point  X=-51584.9302  Y=-11467.2324  Z=   0.0000
          at point  X=-51524.5534  Y=-11924.8549  Z=   0.0000
          at point  X=-51441.2196  Y=-11914.4748  Z=   0.0000
          at point  X=-51418.7527  Y=-12094.8442  Z=   0.0000
          at point  X=-48134.1846  Y=-11660.1059  Z=   0.0000
          at point  X=-47644.0425  Y=-13436.4039  Z=   0.0000
          at point  X=-47179.8782  Y=-17536.8711  Z=   0.0000
          at point  X=-47298.0248  Y=-17547.2504  Z=   0.0000
          at point  X=-47253.3625  Y=-18055.6390  Z=   0.0000
          at point  X=-47456.7920  Y=-18073.5104  Z=   0.0000
          at point  X=-47502.5921  Y=-17590.7028  Z=   0.0000
          at point  X=-47729.5095  Y=-17612.5643  Z=   0.0000
          at point  X=-47665.8742  Y=-18319.3125  Z=   0.0000
          at point  X=-48555.7641  Y=-18405.0457  Z=   0.0000
'''

lines = []
for line in output_autocad.splitlines():
    line = line.strip()
    
    if line.startswith("at point"):
        line = line.replace("at point  X=", "(")
        line = line.replace("  Y=", ", ")
        line = line.replace("  Z=   0.0000", ")")
        lines.append(line)

print("[" + ", ".join(lines) + "]")