local function tikz2image(src, outfile)
  local tmp = os.tmpname()
  local tmpdir = string.match(tmp, "^(.*[\\/])") or "."
  local f = io.open(tmp .. ".tex", 'w')
  f:write("\\documentclass{standalone}\n")
  -- include all packages needed to compile your images
  f:write("\\usepackage{tikz}\n\\usepackage{stanli}\n")
  f:write("\\tikzstyle{termbox} = [draw=black,fill=brown!20,very thick,")
  f:write("rectangle, rounded corners,inner sep=10pt,inner ysep=20pt]\n")
  f:write("\\tikzstyle{termtitle} = [fill=red!5,text=black]\n")
  f:write("\\begin{document}\n")
  f:write(src)
  f:write("\n\\end{document}\n")
  f:close()
  os.execute("pdflatex -output-directory " .. tmpdir  .. " " .. tmp)
  os.execute("vips copy " .. tmp .. ".pdf[dpi=300] " .. outfile)
  os.remove(tmp .. ".tex")
  os.remove(tmp .. ".pdf")
  os.remove(tmp .. ".log")
  os.remove(tmp .. ".aux")
end

local function file_exists(name)
  local f = io.open(name, 'r')
  if f ~= nil then io.close(f); return true
  else return false end
end

function RawBlock(el)
  -- Don't alter element if it's not a tikzpicture environment
  if not el.text:match'^\\begin{tikzpicture}' then
    return nil
    -- Alternatively, parse the contained LaTeX now:
    -- return pandoc.read(el.text, 'latex').blocks
  end  
  local fname = "./build/" .. pandoc.sha1(el.text) .. ".png"
  if not file_exists(fname) then
    tikz2image(el.text, fname)
  end
  return pandoc.Para({pandoc.Image({}, fname)})
end

