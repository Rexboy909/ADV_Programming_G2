import java.util.*;
class T{
static String[][]b=new String[3][3];
static int t;
public static void main(String[]a){
for(String[]r:b)Arrays.fill(r," ");
Scanner s=new Scanner(System.in);
for(;;){
int i=s.nextInt()-1,j=i/3,k=i%3;
b[j][k]="XO".substring(t%2,t%2+1);
for(String[]r:b){for(String c:r)System.out.print(c);System.out.println();}
if(w(b[j][k]))break;
t++;
}
}
static boolean w(String p){
if((b[0][0]==p&b[1][1]==p&b[2][2]==p)|(b[0][2]==p&b[1][1]==p&b[2][0]==p))return 1>0;
for(int i=0;i<3;i++)if((b[i][0]==p&b[i][1]==p&b[i][2]==p)|(b[0][i]==p&b[1][i]==p&b[2][i]==p))return 1>0;
return 0>1;
}
}