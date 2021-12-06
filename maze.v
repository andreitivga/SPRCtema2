//starile principale ale automatului
`define stare_initiala 0
`define pozitie 1
`define verificare_deplasare 2
`define pozitionare 3
`define verificare_pozitie 4
`define verificare_disponibilitate 5

module maze(
input clk,
input [maze_width-1:0]  starting_col, starting_row, 
input maze_in, 
output reg[maze_width-1:0] row, col,
output reg maze_oe,
output reg maze_we, 		
output reg done);	

reg [maze_width-1:0] copie_linie, copie_coloana;
reg [1:0] pozitionare;
reg [4:0] stare_curenta, stare_urm;	 
parameter maze_width = 6;

always @(posedge clk) begin
	if(done == 0)
		stare_curenta <= stare_urm;
end

initial begin
	done = 0;
	stare_urm = `stare_initiala;
end

always @(*) begin
maze_oe = 0;
maze_we = 0;
case(stare_curenta)
	`stare_initiala: begin
		pozitionare = 0;//initil plec spre stanga	
		row = starting_row;
		copie_linie = starting_row;
		col = starting_col;
		copie_coloana = starting_col;
		maze_we = maze_we + 1;
		stare_urm = `pozitie;
	end

	`pozitie: begin 	//aflam directia initiala de plecare		
		if(pozitionare==0) begin
			col=col-1;
		end
		if(pozitionare==1) begin
			col=col+1;
		end
		if(pozitionare==2) begin
			row=row-1;
		end
		if(pozitionare==3) begin
			row=row+1;
		end
		maze_oe = 1;
		stare_urm = `verificare_disponibilitate;
	end
	
	`verificare_pozitie: begin //verific daca am 0 sau 1 in pozitia in care ma aflu
		if(maze_in == 1) begin //ma reintorc de unde am venit si schimb cazul de deplasare
				row = copie_linie;
				col = copie_coloana;
		case(pozitionare) //rotire de 180
				0: pozitionare = 1;
				1: pozitionare = 0;
				2: pozitionare = 3;
				3: pozitionare = 2;
				endcase
				stare_urm = `verificare_deplasare;
		end
		if(maze_in == 0)  begin  //daca am 0 dar nu sunt pe margine
			if(col != 0 && col != 63 && row != 0 && row != 63) begin
				copie_coloana = col; //salvez poz in copii
				copie_linie = row;
				maze_we = 1;
				stare_urm = `verificare_deplasare;
			end
			else begin
			maze_we = 1;
			done = 1;
			end
		end		
	end
	
	`pozitionare: begin
		case(pozitionare)
		0: begin //deplasarea stanga
				if(maze_in == 0) begin
					copie_linie = row;
					copie_coloana = col;
					pozitionare = 2; //schimb cu deplasare sus
				end
				else begin
				row = copie_linie; //ma reintorc
				copie_coloana = col; //salvez pozitia
				col = col - 1; //ma deplasez stanga
				end
			end
		1: begin //deplasare dreapta//verific ce am jos		
				if(maze_in == 0) begin
					copie_linie = row;
					copie_coloana = col;
					pozitionare = 3; //schimb cu dep jos
				end
				else begin
				row = copie_linie; //ma reintorc
				copie_coloana = col; //salvez pozitia
				col = col + 1; //ma deplasez dreapta
				end
			end
		2: begin //deplasare sus
				if(maze_in ==0 ) begin
					copie_coloana = col;
					copie_linie = row;
					pozitionare = 1; // schimb cu deplasare dreapta
				end
				else begin
				col = copie_coloana; //ma reintorc
				copie_linie = row; //salvez pozitia
				row = row - 1;//ma deplasez in sus
				end
			end
		3: begin //deplasare jos
				if(maze_in == 0) begin
					copie_coloana = col;
					copie_linie = row;
					pozitionare = 0; //schimb cu deplasare stanga
				end
				else begin
				col = copie_coloana; // ma reintorc
				copie_linie = row; //salvez pozitia
				row = row + 1; //ma deplasez jos
				end
			end	
	endcase
		maze_oe = 1;
		stare_urm = `verificare_pozitie;
	end
		
	`verificare_disponibilitate: begin 
		if(maze_in == 0) begin //am iesit din start si salvez noua pozitie si in copi
			copie_coloana = col;
			copie_linie = row;
			maze_we = 1;
			stare_urm = `verificare_deplasare;
		end
		else begin 
			pozitionare = pozitionare + 1; //incerc o alta directie
			col = copie_coloana;
			row = copie_linie;
			stare_urm = `pozitie;
		end
	end

	`verificare_deplasare: begin //verificarea pentru deplasarea viitoare		//verific mereu ce am in dreapta(luata in functie de deplasare
		if(pozitionare == 0) begin
			copie_linie = row; //savez poz
			row = row - 1; //verific sus
		end else
		if(pozitionare == 1) begin
			copie_linie = row; //salvez poz
			row = row + 1; //verific jos
		end else
		if(pozitionare == 2) begin
			copie_coloana = col; //salvez poz
			col = col + 1; // verific dreapta
		end else 
		if(pozitionare == 3) begin
			copie_coloana = col; //salvez poz
			col = col - 1; //verific stanga
		end
		maze_oe = 1;
		stare_urm = `pozitionare;
	end
	
endcase
end
endmodule