namespace SharpCifs.Util.Sharpen
{
    public class FileReader : InputStreamReader
	{
		public FileReader (FilePath f) : base(f.GetPath ())
		{
		}
	}
}
