/**
 * Monaco Editor 自定义主题配置
 */

// 白色透明毛玻璃主题
export const whiteGlassTheme = {
  base: 'vs',
  inherit: true,
  rules: [
    { token: '', foreground: '303133', background: 'ffffff00' },
    { token: 'comment', foreground: '909399', fontStyle: 'italic' },
    { token: 'keyword', foreground: '409eff', fontStyle: 'bold' },
    { token: 'string', foreground: '67c23a' },
    { token: 'number', foreground: 'e6a23c' },
    { token: 'function', foreground: '7c3aed' },
    { token: 'variable', foreground: '303133' },
    { token: 'type', foreground: 'f56c6c' },
    { token: 'operator', foreground: '606266' },
  ],
  colors: {
    'editor.background': '#ffffff10',
    'editor.foreground': '#303133',
    'editor.lineHighlightBackground': '#409eff10',
    'editor.selectionBackground': '#409eff30',
    'editor.inactiveSelectionBackground': '#409eff15',
    'editorLineNumber.foreground': '#90939980',
    'editorLineNumber.activeForeground': '#409eff',
    'editorCursor.foreground': '#409eff',
    'editorWhitespace.foreground': '#00000010',
    'editorIndentGuide.background': '#00000010',
    'editorIndentGuide.activeBackground': '#00000020',
  }
}

// 深色透明毛玻璃主题
export const darkGlassTheme = {
  base: 'vs-dark',
  inherit: true,
  rules: [
    { token: '', foreground: 'e0e0e0', background: '00000000' },
    { token: 'comment', foreground: '909399', fontStyle: 'italic' },
    { token: 'keyword', foreground: '409eff', fontStyle: 'bold' },
    { token: 'string', foreground: '67c23a' },
    { token: 'number', foreground: 'e6a23c' },
    { token: 'function', foreground: 'a78bfa' },
    { token: 'variable', foreground: 'e0e0e0' },
    { token: 'type', foreground: 'f56c6c' },
    { token: 'operator', foreground: 'c0c0c0' },
  ],
  colors: {
    'editor.background': '#00000020',
    'editor.foreground': '#e0e0e0',
    'editor.lineHighlightBackground': '#ffffff10',
    'editor.selectionBackground': '#409eff40',
    'editor.inactiveSelectionBackground': '#409eff20',
    'editorLineNumber.foreground': '#ffffff40',
    'editorLineNumber.activeForeground': '#409eff',
    'editorCursor.foreground': '#409eff',
    'editorWhitespace.foreground': '#ffffff10',
    'editorIndentGuide.background': '#ffffff10',
    'editorIndentGuide.activeBackground': '#ffffff20',
  }
}

// 纯白主题
export const pureWhiteTheme = {
  base: 'vs',
  inherit: true,
  rules: [
    { token: '', foreground: '303133' },
    { token: 'comment', foreground: '909399', fontStyle: 'italic' },
    { token: 'keyword', foreground: '409eff', fontStyle: 'bold' },
    { token: 'string', foreground: '67c23a' },
    { token: 'number', foreground: 'e6a23c' },
    { token: 'function', foreground: '7c3aed' },
    { token: 'variable', foreground: '303133' },
    { token: 'type', foreground: 'f56c6c' },
    { token: 'operator', foreground: '606266' },
  ],
  colors: {
    'editor.background': '#ffffff',
    'editor.foreground': '#303133',
    'editor.lineHighlightBackground': '#f5f7fa',
    'editor.selectionBackground': '#409eff30',
    'editor.inactiveSelectionBackground': '#409eff15',
    'editorLineNumber.foreground': '#90939980',
    'editorLineNumber.activeForeground': '#409eff',
    'editorCursor.foreground': '#409eff',
  }
}

// 深色主题（默认）
export const darkTheme = {
  base: 'vs-dark',
  inherit: true,
  rules: [],
  colors: {}
}

// 主题列表
export const editorThemes = [
  {
    id: 'white-glass',
    name: '白色毛玻璃',
    theme: whiteGlassTheme,
    icon: '🤍',
    background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(240, 242, 255, 0.9))',
  },
  {
    id: 'dark-glass',
    name: '深色毛玻璃',
    theme: darkGlassTheme,
    icon: '🖤',
    background: 'linear-gradient(135deg, rgba(30, 30, 30, 0.9), rgba(20, 20, 40, 0.9))',
  },
  {
    id: 'pure-white',
    name: '纯白主题',
    theme: pureWhiteTheme,
    icon: '☀️',
    background: '#ffffff',
  },
  {
    id: 'vs-dark',
    name: '深色主题',
    theme: darkTheme,
    icon: '🌙',
    background: '#1e1e1e',
  }
]

// 获取主题配置
export function getThemeConfig(themeId) {
  return editorThemes.find(t => t.id === themeId) || editorThemes[0]
}

