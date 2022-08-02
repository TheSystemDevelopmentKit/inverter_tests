add wave -position insertpoint  \
sim/:tb_inverter_tests:A \
sim/:tb_inverter_tests:initdone \
sim/:tb_inverter_tests:clock \
sim/:tb_inverter_tests:Z \

run -all
