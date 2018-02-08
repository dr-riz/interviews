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

		//if(cache.size() = cacheSize) removeEldestEntry

		cache.put(104, "104");  
		cache.put(105, "105");  
		cache.put(106, "106");  
		System.out.println("overloading before remove: "+ cache);  

    }

	public static Map<Integer,String> lruCache(final int maxSize) {
		System.out.println("lruCache");
    	return new LinkedHashMap<Integer,String>(maxSize, 0.75f, true) {
        	@Override
        	protected boolean removeEldestEntry(Map.Entry<Integer,String> eldest) {
            	return size() > maxSize;
        	}
        	
   		};
	}

}
