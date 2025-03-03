VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "Sheet1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True

Dim lastHighlight As Range  ' 显式声明为Range对象

Private Sub Worksheet_SelectionChange(ByVal Target As Range)
    ' 限制仅处理单个单元格
    If Target.Count > 1 Then Exit Sub
    
    ' 清除旧高亮
    Cells.Interior.ColorIndex = xlNone
    
    ' 如果点击的是表头或空单元格，退出
    If Target.Row = 1 Or IsEmpty(Target) Then Exit Sub
    
    ' 如果重复点击同一单元格，取消高亮
    If Not lastHighlight Is Nothing Then
        If Target.Address = lastHighlight.Address Then
            Set lastHighlight = Nothing
            Exit Sub
        End If
    End If
    
    ' 获取选中单元格的值
    Dim searchValue As Variant
    searchValue = Target.Value
    
    ' 高亮所有相同内容的单元格
    If searchValue <> "" Then
        Dim cell As Range
        For Each cell In ActiveSheet.UsedRange  ' 明确指定活动工作表
            If cell.Value = searchValue Then
                cell.Interior.Color = RGB(173, 216, 230)  ' 浅蓝色
            End If
        Next cell
    End If
    
    ' 记录当前高亮的位置
    Set lastHighlight = Target
End Sub
