-- This is an inverter_tests VHDL model
-- Initially written by Marko Kosunen
-- Last modification by Marko Kosunen, marko.kosunen@aalto.fi, 16.01.2020 15:51
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.textio.all;


entity inverter_tests is
    port( reset : in std_logic;
          A : in  std_logic;
          Z : out std_logic
        );
end inverter_tests;

architecture rtl of inverter_tests is
begin
    invert:process(A)
    begin
        Z<=NOT A;
    end process;
end architecture;

