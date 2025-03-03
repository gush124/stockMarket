Attribute VB_Name = "模块1"
Sub ImportTop10Plates()
    On Error GoTo ErrorHandler
    Dim conn As Object, rs As Object
    Dim sql As String, connStr As String
    Dim i As Integer, targetCol As Integer
    Dim lastUpdate As Date
    
    ' 创建数据库连接对象
    Set conn = CreateObject("ADODB.Connection")
    Set rs = CreateObject("ADODB.Recordset")
    
    ' 数据库连接字符串（根据实际修改）
    connStr = "DRIVER={MySQL ODBC 9.2 Unicode Driver};" & _
              "SERVER=localhost;" & _
              "DATABASE=stock;" & _
              "UID=root;" & _
              "PWD=123456;" & _
              "PORT=3306;"
    
    ' 打开数据库连接
    conn.Open connStr
    
' 获取最新更新时间
    sql = "SELECT MAX(update_time) FROM stock_plates"
    Set rs = conn.Execute(sql)
    If Not rs.EOF Then
        lastUpdate = rs.Fields(0).Value
    Else
        MsgBox "未找到更新时间", vbExclamation
        Exit Sub
    End If
    rs.Close
    
    ' 获取强度前10的板块
    sql = "SELECT plate_name FROM stock_plates WHERE update_time = '" & _
          Format(lastUpdate, "yyyy-mm-dd hh:mm:ss") & "' " & _
          "ORDER BY strength DESC LIMIT 10"
    Set rs = conn.Execute(sql)
    
    ' 在 A 列前面插入新列
    Columns(1).Insert Shift:=xlToRight
    
    ' 写入数据到新插入的列（第 1 列）
    With ActiveSheet
        ' 写入标题日期
        .Cells(1, 1).Value = Format(lastUpdate, "yyyy/m/d")
        
        ' 写入板块数据
        i = 2
        Do While Not rs.EOF And i <= 11 ' 行 2 到 11，共10条数据
            .Cells(i, 1).Value = rs.Fields("plate_name").Value
            rs.MoveNext
            i = i + 1
        Loop
        
        ' 不足10条时填充空值
        For i = i To 11
            .Cells(i, 1).Value = ""
        Next i
    End With

Cleanup:
    ' 清理资源
    If rs.State = 1 Then rs.Close
    If conn.State = 1 Then conn.Close
    Set rs = Nothing
    Set conn = Nothing
    Exit Sub

ErrorHandler:
    MsgBox "错误 " & Err.Number & ": " & Err.Description, vbCritical
    Resume Cleanup
End Sub
