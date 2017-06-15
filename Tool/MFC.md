# CTreeCtrl https://msdn.microsoft.com/en-us/library/8bkz91b4.aspx

* 几个关键的数据结构和类型：

	* HTREEITEM
	* TVITEM

		```
		typedef struct tagTVITEM {
		  UINT      mask;
		  HTREEITEM hItem;
		  UINT      state;
		  UINT      stateMask;
		  LPTSTR    pszText;
		  int       cchTextMax;
		  int       iImage;
		  int       iSelectedImage;
		  int       cChildren;
		  LPARAM    lParam;
		} TVITEM, *LPTVITEM;
		```

* 如何获得当前选中: GetSelectedItem()
* 获取对应的项：GetItem(TVITEM*)，指明TVITEM的成员，可以获取指定项的内容

* 如何添加项，并在项中附加一些自己的信息。

```
HTREEITEM InsertItem(LPTVINSERTSTRUCT lpInsertStruct);

 
HTREEITEM InsertItem(
    UINT nMask,  
    LPCTSTR lpszItem,  
    int nImage,  
    int nSelectedImage,  
    UINT nState,  
    UINT nStateMask,  
    LPARAM lParam,  
    HTREEITEM hParent,  
    HTREEITEM hInsertAfter);

 
HTREEITEM InsertItem(
    LPCTSTR lpszItem,  
    HTREEITEM hParent = TVI_ROOT,  
    HTREEITEM hInsertAfter = TVI_LAST);

 
HTREEITEM InsertItem(
    LPCTSTR lpszItem,  
    int nImage,  
    int nSelectedImage,  
    HTREEITEM hParent = TVI_ROOT,  
    HTREEITEM hInsertAfter = TVI_LAST);
```

```
HTREEITEM item = m_ctrlSecTree.InsertItem(TVIF_TEXT | TVIF_PARAM, _T("慧鱼卷边槽钢")
	, 0, 0, 0, 0, LPARAM(SectorType_HY_CHANNEL_CURLING), TVI_ROOT, NULL);
```


# CListCtrl https://msdn.microsoft.com/en-us/library/hfshke78.aspx

* 如何设置选中
* 处理选择的消息：需要将控件的 Always show selection 设置为TRUE，在没有激活的时候仍然高亮显示选中的项。

```
m_list.SetItemState(index,LVNI_FOCUSED | LVIS_SELECTED, LVNI_FOCUSED | LVIS_SELECTED)
```

* 选中整行：

```
m_ctrlSecSpec.SetExtendedStyle(m_ctrlSecSpec.GetExtendedStyle() | LVS_EX_FULLROWSELECT);
```

* 获取列数：

	```
	int n = m_List.GetHeaderCtrl()->GetItemCount();

	```

* 自动行宽度：所有的行都添加好了之后再对每一行调用 SetColumnWidth(nCol, LVSCW_AUTOSIZE_USEHEADER)