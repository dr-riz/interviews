import java.util.*;

public class LRUCache {

	static int cacheSize = 3;

    public static void main(String[] args) {
        System.out.println("LRUCache");

//		myCache = lruCache(cacheSize);
		Map<Integer,String> cache = lruCache(3);
		System.out.println(cache.size());
		
		cache.put(101,"Let us C");  
   		cache.put(102, "Operating System");  
   		cache.put(103, "Data Communication and Networking");  
   		System.out.println("Values before remove: "+ cache);   

		cache.put(104, "104");  
		System.out.println("Values before remove: "+ cache);  

    }

	public static Map<Integer,String> lruCache(final int maxSize) {
		System.out.println("lruCache");
    	return new LinkedHashMap<Integer,String>(maxSize*4/3, 0.75f, true) {
        	@Override
        	protected boolean removeEldestEntry(Map.Entry<Integer,String> eldest) {
            	return size() > maxSize;
        	}
   		};
	}

}
