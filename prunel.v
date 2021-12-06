module maze(
	input 		clk,
	input[5:0] 	starting_col, starting_row, 		// indicii punctului de start
	input 		maze_in, 							// oferã informa?ii despre punctul de coordonate [row, col]
	output   reg[5:0] row, col, 							// selecteazã un rând si o coloanã din labirint
	output 	reg	maze_oe,							// output enable (activeazã citirea din labirint la rândul ?i coloana date) - semnal sincron
	output 	reg	maze_we, 							// write enable (activeazã scrierea în labirint la rândul ?i coloana  date) - semnal sincron
	output 	reg	done);      // ie?irea din labirint a fost gasitã; semnalul rãmane activ

//starile principale ale automatului
`define stare_initiala       0
`define start           1
`define verstart        2
`define verificare_deplasare          3
`define pozitionare             4
`define verificare_pozitie          8
`define stare_finala            9



reg [5:0] copie_linie, copie_coloana;  //copiile coordonatelor, folosite pentru a retine starea anterioara
reg [1:0] pozitionare; //Eu am ales directiile ca si cand as privi matricea pe foaie.
		//directie deplasare:
			//  0->dreapta
			//  1->stanga
			//  2->jos
			//  3->sus


reg [4:0] stare_curenta, stare_urm ; 	//starile automatului

always @(posedge clk) begin
	if(done == 0)
		stare_curenta <= stare_urm;
end

always @(*) begin
    stare_urm = `stare_initiala;
	 maze_we = 0;
	 maze_oe = 0;
	 done = 0;
	 case(stare_curenta)
			`stare_initiala: begin

				pozitionare = 0;//initil plec spre dreapta
				maze_we = 1;
				row = starting_row;
				col = starting_col;
				copie_linie = starting_row;
				copie_coloana = starting_col;

				stare_urm = `start;
			end


			`start : begin
				//aflam directia initiala de plecare
				case(pozitionare)
					0: col = col + 1; //drepta
					1: col = col - 1; //stanga
					2: row = row + 1; //jos
					3: row = row - 1; //sus
				endcase
				maze_oe = 1;
				stare_urm =  `verstart;

				end


			`verstart: begin
				if(maze_in == 0) begin //am iesit din start si salvez noua pozitie si in copi
					copie_coloana = col;
					copie_linie = row;
					maze_we = 1;

					stare_urm = `verificare_deplasare;
				end

				if(maze_in == 1) begin //ma reintorc in start;
					pozitionare = pozitionare + 1; //incerc o alta directie
					col = copie_coloana;
					row = copie_linie;

					stare_urm = `start;

				end

			end


			`verificare_deplasare: begin //verificarea pentru deplasarea viitoare
				//verific mereu ce am in dreapta(luata in functie de deplasare)
				case(pozitionare)
					0: begin //dreapta
						copie_linie = row; //salvez poz
						row = row + 1; //verific jos


					end

					1: begin //stanga
						copie_linie = row; //savez poz
						row = row - 1; //verific sus


					end

					2: begin //jos
						copie_coloana = col; //salvez poz
						col = col - 1; //verific stanga


					end

					3: begin //sus
						copie_coloana = col; //salvez poz
						col = col + 1; // verific dreapta

					end

				endcase
				maze_oe = 1;
				stare_urm = `pozitionare;

			end

			`verificare_pozitie: begin //verific daca am 0 sau 1 in pozitia in care ma aflu

				if(maze_in == 0)  begin

					if(col == 0 || col == 63 || row == 0 || row == 63) begin

						maze_we = 1;
						stare_urm = `stare_finala;

					end

					else begin //daca am 0 dar nu sunt pe margine
						copie_coloana = col; //salvez poz in copi
						copie_linie = row;
						maze_we = 1;
						stare_urm = `verificare_deplasare;
					end
				end

				if(maze_in == 1) begin //ma reintorc de unde am venit si schimb cazul de deplasare
					row = copie_linie;
					col = copie_coloana;
					//conditie de deplasare noua
					case(pozitionare) //rotire de 180
						0: pozitionare = 1;
						1: pozitionare = 0;
						2: pozitionare = 3;
						3: pozitionare = 2;
					endcase


					stare_urm = `verificare_deplasare;
				end

			end

			`pozitionare: begin
				case(pozitionare)
					0: begin //deplasare dreapta
						//verific ce am jos
						if(maze_in == 1) begin
							row = copie_linie; //ma reintorc
							copie_coloana = col; //salvez pozitia
							col = col + 1; //ma deplasez dreapta

						end

						if(maze_in == 0)  begin //raman si salvez coordonatele in copi
							copie_linie = row;
							copie_coloana = col;
							pozitionare = 2; //schimb cu dep jos

						end

					end

					1: begin //deplasarea stanga

						if(maze_in == 1) begin
							row = copie_linie; //ma reintorc
							copie_coloana = col; //salvez pozitia
							col = col - 1; //ma deplasez stanga

						end

						if(maze_in == 0) begin //raman si salvez coordoatele in copi
							copie_linie = row;
							copie_coloana = col;
							pozitionare = 3; //schimb cu deplasare sus

						end

					end

					2: begin //deplasare jos
						if(maze_in == 1) begin
							col = copie_coloana; // ma reintorc
							copie_linie = row; //salvez pozitia
							row = row + 1; //ma deplasez jos

						end

						if(maze_in == 0) begin //raman si salvez coordonatele in copi
							copie_coloana = col;
							copie_linie = row;
							pozitionare = 1; //schimb cu deplasare stanga

						end

					end

					3: begin //deplasare sus
						if(maze_in == 1) begin
							col = copie_coloana; //ma reintorc
							copie_linie = row; //salvez pozitia
							row = row - 1;//ma deplasez in sus

						end


						if(maze_in == 0) begin //raman si salvez noile coordonate in copi
							copie_coloana = col;
							copie_linie = row;
							pozitionare = 0; // schimb cu deplasare dreapta

						end

					end
				endcase
				maze_oe = 1;
				stare_urm = `verificare_pozitie;
			end

			`stare_finala: done = 1; //Am iesit!

			default: ;

	endcase

end

endmodule