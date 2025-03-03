Attribute VB_Name = "ģ��1"
Sub ImportTop10Plates()
    On Error GoTo ErrorHandler
    Dim conn As Object, rs As Object
    Dim sql As String, connStr As String
    Dim i As Integer, targetCol As Integer
    Dim lastUpdate As Date
    
    ' �������ݿ����Ӷ���
    Set conn = CreateObject("ADODB.Connection")
    Set rs = CreateObject("ADODB.Recordset")
    
    ' ���ݿ������ַ���������ʵ���޸ģ�
    connStr = "DRIVER={MySQL ODBC 9.2 Unicode Driver};" & _
              "SERVER=localhost;" & _
              "DATABASE=stock;" & _
              "UID=root;" & _
              "PWD=123456;" & _
              "PORT=3306;"
    
    ' �����ݿ�����
    conn.Open connStr
    
' ��ȡ���¸���ʱ��
    sql = "SELECT MAX(update_time) FROM stock_plates"
    Set rs = conn.Execute(sql)
    If Not rs.EOF Then
        lastUpdate = rs.Fields(0).Value
    Else
        MsgBox "δ�ҵ�����ʱ��", vbExclamation
        Exit Sub
    End If
    rs.Close
    
    ' ��ȡǿ��ǰ10�İ��
    sql = "SELECT plate_name FROM stock_plates WHERE update_time = '" & _
          Format(lastUpdate, "yyyy-mm-dd hh:mm:ss") & "' " & _
          "ORDER BY strength DESC LIMIT 10"
    Set rs = conn.Execute(sql)
    
    ' �� A ��ǰ���������
    Columns(1).Insert Shift:=xlToRight
    
    ' д�����ݵ��²�����У��� 1 �У�
    With ActiveSheet
        ' д���������
        .Cells(1, 1).Value = Format(lastUpdate, "yyyy/m/d")
        
        ' д��������
        i = 2
        Do While Not rs.EOF And i <= 11 ' �� 2 �� 11����10������
            .Cells(i, 1).Value = rs.Fields("plate_name").Value
            rs.MoveNext
            i = i + 1
        Loop
        
        ' ����10��ʱ����ֵ
        For i = i To 11
            .Cells(i, 1).Value = ""
        Next i
    End With

Cleanup:
    ' ������Դ
    If rs.State = 1 Then rs.Close
    If conn.State = 1 Then conn.Close
    Set rs = Nothing
    Set conn = Nothing
    Exit Sub

ErrorHandler:
    MsgBox "���� " & Err.Number & ": " & Err.Description, vbCritical
    Resume Cleanup
End Sub
