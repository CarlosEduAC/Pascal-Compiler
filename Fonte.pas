program funcoes;
const TAM = 10.0;
type
	vetor = array[15] of integer;
	aluno = record
			nota1, nota2 : real;
		end;
var
	A, C : real; 
	B, D : integer;
	E : vetor;
	F : aluno;
// Isto é um comentário no Pascal
function fatorial(a:integer;) : integer
var i : integer;
begin
	i := 1;
	result:= 1;
	while i < a
	begin
		result:=result*i;
		i:=i+1;
	end;
end
{
	Outra forma de comentário no Pascal
}
function exp(a: real; b: integer;) : real
var i : integer;
begin
	i := 1;
	result := a;
	if b = 0 then
		result := 1 
	else
		while i < b
		begin
			result := a * a;
			i := i + 1;
		end
end
function lerDados() : aluno
begin
	write "digite as notas do aluno";
	read result.nota1;
	read result.nota2;
end
function maior(a : vetor;) : integer
var i : integer;
begin
	i := 0;
	result := a[0];
	while i < 15
	begin
		if a[i] > result then
			result := a[i];
	end;
end

begin
	A:=TAM;
	B := fatorial(D);
	C := exp(A,B);
	D := maior(E);
	F := lerDados();
end