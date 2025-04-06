Here is a simple flow chart:

```mermaid
graph TD;
    A[Code 1]-->B[Code 2
    Code 2b];
    A-->C[x=1;];
    B-->D[Code 4<br>Line 2];
    C-->D;
    D--label-->E["Code (4)
Line 2"];
    E-->F["`**Code 4**<br>Line 2`"];
```

```mermaid
graph TD;
    A["for i=1,10 {<br>print i*i;<br>}"]
    B["<div align='left'>for i=1,10 {<br>   print i*i;<br>}</div>"];
    C["<div align='left'>for i=1,10 {<br>&nbsp;&nbsp;&nbsp;print i*i;<br>}</div>"];
    A-->B-->C
```

```mermaid
graph TD;
    A["for i=1,10 {<br>print i*i;<br>}"]
    B["Program(statements=[For(name=Name(str='i'), startval=Integer(n=1), endval=Integer(n=10), statements=[Print(value=Multiply(left=Name(str='i'), right=Name(str='i')))])])"];
    C["<div align='left'>for i=1,10 {<br>&nbsp;&nbsp;&nbsp;print i*i;<br>}</div>"];
    A-->B-->C
```
